from constants import (
    TCONTEXT,
    FROM_SAG,
    TO_SAG,
    LOCAL_LRT_PATH,
    REMOTE_LRT_PATH,
    LOG_PATH,
    VSR_HOST,
)
from myfunctions import (
    validate_lrt_B,
    gunzip_lrt,
    gzip_lrt,
    modify_lrt_sag,
    logging,
    initiate_logfile,
)
from sftp_socks import download_lrt_B, upload_lrt_B


initiate_logfile("LGHR", LOG_PATH)

download_lrt_B(VSR_HOST, LOCAL_LRT_PATH, REMOTE_LRT_PATH)

list_B = validate_lrt_B(LOCAL_LRT_PATH)

for lrt in list_B:
    logging.info("Working in LRT: {}".format(lrt))
    lrt_1 = gunzip_lrt(lrt)
    modify_lrt_sag(lrt_1, TCONTEXT, FROM_SAG, TO_SAG)
    lrt_2 = gzip_lrt(lrt_1)
    logging.info("Process completed for LRT {}\n".format(lrt_2))

# upload_lrt_B(VSR_HOST, constants.LOCAL_LRT_PATH, constants.REMOTE_LRT_PATH)