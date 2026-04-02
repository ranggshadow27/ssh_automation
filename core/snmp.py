import asyncio
import re
import logging

try:
    from pysnmp.hlapi.v3arch.asyncio import get_cmd, CommunityData, UdpTransportTarget, ContextData, SnmpEngine, ObjectType, ObjectIdentity
except ImportError as e:
    print(f"Error importing pysnmp.hlapi.v3arch.asyncio: {str(e)}. SNMP functionality will be disabled.")
    logging.error(f"Error importing pysnmp.hlapi.v3arch.asyncio: {str(e)}")
    get_cmd = SnmpEngine = CommunityData = UdpTransportTarget = ContextData = ObjectType = ObjectIdentity = None

async def async_detect_router_type_snmp(ip, community='MHGISPNet'):
    if get_cmd is None:
        error_msg = f"SNMP disabled: pysnmp.hlapi.v3arch.asyncio import failed"
        print(error_msg)
        logging.error(error_msg)
        return "Unknown"
    try:
        error_indication, error_status, error_index, var_binds = await get_cmd(
            SnmpEngine(),
            CommunityData(community),
            await UdpTransportTarget.create((ip, 161), timeout=10, retries=3),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'))
        )
        if error_indication or error_status:
            error_msg = f"‣ SNMP error untuk {ip}: {error_indication or error_status.prettyPrint()}"
            print(error_msg)
            logging.error(error_msg)
            return "Unknown"
        sys_descr = str(var_binds[0][1])
        print(f"‣ Router Type: {sys_descr}")
        if re.search(r'RouterOS|RB450Gx4', sys_descr, re.IGNORECASE):
            return "Mikrotik"
        elif re.search(r'Linux', sys_descr, re.IGNORECASE):
            return "Grandstream"
        return "Unknown"
    except Exception as e:
        error_msg = f"SNMP exception untuk {ip}: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        return "Unknown"

def detect_router_type_snmp(ip, community='MHGISPNet'):
    print(f"‣ Checking router type for {ip} ...")
    return asyncio.run(async_detect_router_type_snmp(ip, community))