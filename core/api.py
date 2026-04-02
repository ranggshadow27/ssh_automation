import requests
import logging

def fetch_all_site_data():
    api_urls = [
        "https://api.snt.co.id/v2/api/mhg-rtgs/terminal-data-h10/mhg",
        "https://api.snt.co.id/v2/api/mhg-rtgs/terminal-data-h58/mhg",
        "https://api.snt.co.id/v2/api/mhg-rtgs/terminal-data-h47/mhg"
    ]
    site_data = {}
    for api_url in api_urls:
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json().get("data", [])
            for item in data:
                site_id = item["terminal_id"]
                if site_id not in site_data:
                    site_data[site_id] = item
        except requests.exceptions.RequestException as e:
            error_msg = f"Gagal fetch API {api_url}: {str(e)}"
            logging.error(error_msg)
            print(error_msg)
    print(f"‣ Berhasil fetch data untuk {len(site_data)} site dari API.")
    return site_data

def check_site_status(site_id, site_data):
    item = site_data.get(site_id)
    if not item:
        return "Site Down", f"Site ID {site_id} tidak ditemukan di API"
    
    modem_status = item.get("modem", "Down")
    mikrotik_status = item.get("mikrotik", "Down")
    print(f"‣ Status Modem & Router : {modem_status} | {mikrotik_status}")
    
    if modem_status == "Up" and mikrotik_status == "Up":
        return "Up", ""
    elif modem_status == "Up" and mikrotik_status == "Down":
        return "Router Down", ""
    else:
        return "Site Down", ""