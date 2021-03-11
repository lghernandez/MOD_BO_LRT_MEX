from constants import (
    REMOTE_LRT_PATH,
    LOG_PATH,
    VALIDATE_LRT_PATH,
    VSRS,
)
from functions_validate_lrt import (
    gunzip_lrt,
    validate_lrt_all,
    logging,
    create_custom_logger,
    validate_lrt_format,
    remove_file_by_extension,
)
from sftp_socks import download_lrt_all_with_logger
import os

for vsr_name, vsr_ip in VSRS.items():
    vsr_path = os.path.join(VALIDATE_LRT_PATH, vsr_name)
    remove_file_by_extension(vsr_path, ".xml")
    my_logger = create_custom_logger(vsr_name, LOG_PATH)
    download_lrt_all_with_logger(vsr_ip, vsr_path, REMOTE_LRT_PATH, my_logger)
    list_LRT = validate_lrt_all(vsr_path, my_logger)
    for lrt in list_LRT:
        lrt_1 = gunzip_lrt(lrt, my_logger)
        if lrt_1 is not None:
            validate_lrt_format(lrt_1, my_logger)