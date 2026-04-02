import pandas as pd
import logging
import time
from .api import fetch_all_site_data, check_site_status
from .snmp import detect_router_type_snmp
from .ssh import execute_mikrotik_command
from .utils import increment_ip

def has_unknown_router_types(df):
    return df['router_type'].isin(["", "Unknown"]).any() or df['router_type'].isna().any()

def process_batch(df, excel_file, mikrotik_user, mikrotik_pass, snmp_community, use_increment_ip, site_data):
    total_data = len(df)
    print(f"Total Data yang akan di proses: {total_data}")
    
    for index, row in df.iterrows():
        site_id = str(row["site_id"]).strip()
        ip = str(row["ip_address"]).strip()
        commands = str(row["command"]).strip()
        router_type = str(row.get("router_type", "")).strip()
        status = str(row.get("status", "")).strip()
        
        print(f"\nMemproses site_id {site_id} (Progression: {index + 1} of {total_data})")
        
        # Cek SNMP jika router_type kosong atau Unknown
        if router_type in ["", "Unknown"]:
            ip_to_use_snmp = increment_ip(ip) if use_increment_ip else ip
            new_router_type = detect_router_type_snmp(ip_to_use_snmp, snmp_community)
            df.at[index, "router_type"] = new_router_type
            router_type = new_router_type
            
            try:
                df.to_excel(excel_file, index=False)
            except Exception as e:
                logging.error(f"Gagal menyimpan Excel: {str(e)}")
                print(f"Error: Gagal menyimpan file Excel: {str(e)}")
                print(f"Error: Mohon untuk menutup file Excel anda: {str(e)}")
                continue
        
        # Cek status dari API cache
        api_status, api_output = check_site_status(site_id, site_data)
        
        # Hanya proses logic SSH jika router_type bukan Unknown/kosong dan status bukan Success
        if router_type not in ["", "Unknown"] and status != "Success":
            df.at[index, "status"] = api_status
            df.at[index, "output"] = api_output if api_output else ""
            
            try:
                df.to_excel(excel_file, index=False)
            except Exception as e:
                logging.error(f"Gagal menyimpan Excel: {str(e)}")
                print(f"Error: Gagal menyimpan file Excel: {str(e)}")
                print(f"Error: Mohon untuk menutup file Excel anda: {str(e)}")
                continue
            
            if api_status != "Up":
                print(f"Status {site_id}: {api_status} ❌")
                continue
            
            if router_type != "Mikrotik":
                print(f"‣ Skipping SSH for {site_id} | {ip} (router_type: {router_type}) ❕")
                continue
            
            ip_to_use = increment_ip(ip) if use_increment_ip else ip
            print(f"‣ Using IP: {ip_to_use}")
            
            ssh_status, ssh_output = execute_mikrotik_command(ip_to_use, commands, mikrotik_user, mikrotik_pass)
            df.at[index, "status"] = ssh_status
            df.at[index, "output"] = ssh_output
            
            try:
                df.to_excel(excel_file, index=False)
            except Exception as e:
                logging.error(f"Gagal menyimpan Excel: {str(e)}")
                print(f"Error: Gagal menyimpan file Excel: {str(e)}")
                print(f"Error: Mohon untuk menutup file Excel anda: {str(e)}")
        else:
            print(f"‣ Skipping site_id {site_id} (router_type: {router_type}, status: {status})")