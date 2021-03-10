from constants import (
    REMOTE_LRT_PATH,
    LOG_PATH,
)
from myfunctions import (
    gunzip_lrt,
    validate_lrt_all,
    logging,
    initiate_logfile,
    validate_lrt_format,
)
from sftp_socks import download_lrt_all

local_path = "D:\\TBS\\Archivos LRTs SRs Clientes\\All-LRTs"
vsr_host = "192.168.179.7"

vsrs = {
    "vsrmiabr3": "192.168.229.181",
    "vsrmiatc3": "192.168.229.218",
    "vsrloneq3": "192.168.229.56",
    "vsralhta3": "192.168.229.82",
    "vsrhkgeq3": "192.168.179.6",
    "vsrhkgeq4": "192.168.179.7",
}

initiate_logfile("Validate_LRT", LOG_PATH)

download_lrt_all(vsr_host, local_path, REMOTE_LRT_PATH)

list_LRT = validate_lrt_all(local_path)

for lrt in list_LRT:
    lrt_1 = gunzip_lrt(lrt)
    validate_lrt_format(lrt_1)