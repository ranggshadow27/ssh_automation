import logging

# Setup logging
logging.basicConfig(
    filename='mikrotik_ssh_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DEFAULT_SNMP_COMMUNITY = "MHGISPNet"