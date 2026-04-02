import pandas as pd
import time
import logging
from ui.console import print_welcome_message, get_credentials, prompt_increment_ip, print_summary
from ui.file_browser import browse_excel_file
from core.processor import process_batch, has_unknown_router_types
from core.api import fetch_all_site_data

def main():
    try:
        print_welcome_message()
        excel_file = browse_excel_file()
        print(f"File Excel dipilih: {excel_file}")
        
        df = pd.read_excel(excel_file, dtype={"status": "object", "output": "object", "router_type": "object"})
        required_columns = ["site_id", "ip_address", "command"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Kolom '{col}' tidak ditemukan di Excel!")
        
        if "status" not in df.columns:
            df["status"] = pd.Series(dtype="object")
        if "output" not in df.columns:
            df["output"] = pd.Series(dtype="object")
        if "router_type" not in df.columns:
            df["router_type"] = pd.Series(dtype="object")
        
        df["status"] = df["status"].fillna("")
        df["output"] = df["output"].fillna("")
        df["router_type"] = df["router_type"].fillna("")

        mikrotik_user, mikrotik_pass, snmp_community = get_credentials()
        use_increment_ip = prompt_increment_ip()
        print(f"Fitur +1 ip_address: {'Aktif' if use_increment_ip else 'Tidak aktif'}")
        
        while True:
            site_data = fetch_all_site_data()
            process_batch(df, excel_file, mikrotik_user, mikrotik_pass, snmp_community, use_increment_ip, site_data)
            
            df = pd.read_excel(excel_file, dtype={"status": "object", "output": "object", "router_type": "object"})
            df["status"] = df["status"].fillna("")
            df["output"] = df["output"].fillna("")
            df["router_type"] = df["router_type"].fillna("")

            if not has_unknown_router_types(df):
                print_summary(df)
                break
            else:
                print("\n↻ Masih ada router_type Unknown/kosong. Menunggu 5 menit untuk cek ulang...")
                time.sleep(300)
    
    except Exception as e:
        logging.error(f"Error di main program: {str(e)}")
        print(f"‣ Error: Program gagal: {str(e)}. Cek log untuk detail.")
        raise

if __name__ == "__main__":
    main()