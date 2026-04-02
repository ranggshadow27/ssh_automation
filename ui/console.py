import inquirer
from getpass import getpass
from config import DEFAULT_SNMP_COMMUNITY

def print_welcome_message():
    print("┃" * 50)
    print("┃" + " " * 48 + "┃")
    print("┃" + " " * 23 + "🤖" + " " * 23 + "┃")
    print("┃" + " " * 10 + "Welcome to Mikrotik SSH App" + " " * 11 + "┃")
    print("┃" + " " * 19 + "©ratipray27" + " " * 18 + "┃")
    print("┃" + " " * 48 + "┃")
    print("┃" * 50)
    print("\nSilahkan tekan Enter untuk memilih file Excel...")
    input()

def get_credentials():
    try:
        print("Masukkan kredensial Router:")
        mikrotik_user = input("• Username Mikrotik: ") or ""
        mikrotik_pass = getpass("• Password Mikrotik: ") or ""
        snmp_community = input(f"• SNMP Community [{DEFAULT_SNMP_COMMUNITY}]: ") or DEFAULT_SNMP_COMMUNITY
        return mikrotik_user, mikrotik_pass, snmp_community
    except Exception as e:
        import logging
        logging.error(f"Error saat input kredensial: {str(e)}")
        print(f"‣ Error: Gagal memasukkan kredensial: {str(e)}")
        raise

def prompt_increment_ip():
    try:
        questions = [
            inquirer.List('increment',
                        message="Apakah ingin menggunakan fitur +1 ip_address?",
                        choices=['Ya', 'Tidak'],
                        default='Tidak')
        ]
        answers = inquirer.prompt(questions)
        return answers['increment'] == 'Ya'
    except Exception as e:
        import logging
        logging.error(f"‣ Error saat prompt increment IP: {str(e)}")
        print(f"‣ Error: Gagal memilih opsi increment IP: {str(e)}")
        raise

def print_summary(df):
    total_data = len(df)
    counts = df['router_type'].value_counts()
    grandstream_count = counts.get("Grandstream", 0)
    mikrotik_count = counts.get("Mikrotik", 0)
    unknown_count = counts.get("Unknown", 0)
    print(f"Selesai memproses data {total_data}, detail : {grandstream_count} Grandstream, {mikrotik_count} Mikrotik, {unknown_count} Unknown")