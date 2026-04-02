from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import logging
import time

def execute_mikrotik_command(ip, commands, username, password, retries=2, delay=0.25):
    for attempt in range(1, retries + 1):
        try:
            device = {
                "device_type": "mikrotik_routeros",
                "ip": ip,
                "username": username,
                "password": password,
                "port": 22,
                "timeout": 30,
                "conn_timeout": 30
            }
            with ConnectHandler(**device) as conn:
                logging.info(f"Successfully connect to {ip}")
                print(f"‣ Successfully connect to {ip}")
                display_commands = commands if len(commands) <= 100 else commands[:100] + "..."
                print(f"‣ Applying Command to {ip}:\n{display_commands}")
                output = conn.send_config_set(commands.split("\n"))
                logging.info(f"Command untuk {ip} berhasil: {display_commands}")
                print(f"‣ Command for {ip} Success ✅")
                return "Success", output
        except NetmikoTimeoutException as e:
            error_msg = f"Error: Timeout ke {ip} (attempt {attempt}/{retries})"
            print(f"‣ Error: Timeout ke {ip} (attempt {attempt}/{retries}) ❌")
            logging.error(error_msg + f": {str(e)}")
            if attempt == retries:
                return error_msg, error_msg
            time.sleep(delay)
        except NetmikoAuthenticationException as e:
            error_msg = f"‣ Error: Autentikasi gagal untuk {ip}"
            print(f"‣ Error: Autentikasi gagal untuk {ip} ❌")
            logging.error(error_msg + f": {str(e)}")
            return error_msg, error_msg
        except Exception as e:
            error_msg = f"‣ Error: {str(e)}"
            print(f"‣ Unknown Error {ip} ❌")
            logging.error(error_msg + f": {str(e)}")
            if "Error reading SSH protocol banner" in str(e) and attempt < retries:
                logging.warning(f"Retrying connection to {ip} due to SSH banner error")
                time.sleep(delay)
            else:
                return error_msg, error_msg