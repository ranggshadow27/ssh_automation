import logging

def increment_ip(ip):
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            raise ValueError(f"IP tidak valid: {ip}")
        last_octet = int(parts[-1])
        if last_octet >= 255:
            raise ValueError(f"Tidak bisa increment IP {ip}: oktet terakhir sudah maksimum (255)")
        parts[-1] = str(last_octet + 1)
        return '.'.join(parts)
    except Exception as e:
        logging.error(f"Gagal increment IP {ip}: {str(e)}")
        raise ValueError(f"Gagal increment IP {ip}: {str(e)}")