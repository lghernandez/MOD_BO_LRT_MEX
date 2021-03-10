from constants import (
    REMOTE_LRT_PATH,
    LOG_PATH,
    VSR_HOST,
)

from myfunctions import (
    gunzip_lrt,
    gzip_lrt,
    logging,
    initiate_logfile,
)
from sftp_socks import download_lrt_all
import os
from lxml import etree

my_path = "D:\\TBS\\Archivos LRTs SRs Clientes\\All-LRTs"

initiate_logfile("Validate_LRT", LOG_PATH)

download_lrt_all(VSR_HOST, my_path, REMOTE_LRT_PATH)

# list_LRT = validate_lrt_B(LOCAL_LRT_PATH)

# for lrt in list_LRT:
#     logging.info("Working in LRT: {}".format(lrt))
#     lrt_1 = gunzip_lrt(lrt)
#     modify_lrt_sag(lrt_1, TCONTEXT, FROM_SAG, TO_SAG)
#     lrt_2 = gzip_lrt(lrt_1)
#     logging.info("Process completed for LRT {}\n".format(lrt_2))


list_lrt = os.listdir(path=my_path)

print(list_lrt)

for lrt in list_lrt:
    lrt_1 = my_path + "\\" + lrt
    try:
        xmlschema = etree.XMLSchema(file="validate.xsd")
        tree = etree.parse(lrt_1)
    except etree.XMLSyntaxError as e:
        e_str = str(e)
        print(
            "The file {} has syntax errors, first error found is: {}".format(
                lrt_1, e_str.split("(")[0]
            )
        )
    else:
        if xmlschema.validate(tree):
            print("The file {} is well formed and valid".format(lrt_1))
        else:
            try:
                xmlschema.assertValid(tree)
            except etree.DocumentInvalid as e:
                print("The file {} is well formed but invalid: {}".format(lrt_1, e))
