from constants import (
    TCONTEXT,
    FROM_SAG,
    TO_SAG,
    EMAIL_FROM,
    EMAIL_TO,
    LOCAL_LRT_PATH,
    REMOTE_LRT_PATH,
    LOG_PATH,
    VSRS_MOD_B,
)
from myfunctions import (
    validate_lrt_B_with_logger,
    gunzip_lrt_with_logger,
    gzip_lrt_with_logger,
    modify_lrt_sag_with_logger,
    logging,
)
from email_notification import (
    service_account_login,
    create_message_html_with_attachment,
    send_message,
)
from functions_validate_lrt import remove_file_by_extension, create_custom_logger
from sftp_socks import download_lrt_B_with_logger, upload_lrt_B_with_logger
from telegram_notifications import send_telegram_message
import os, shutil

for vsr_name, vsr_ip in VSRS_MOD_B.items():
    vsr_logname = "MOD_B_" + vsr_name
    vsr_backup = vsr_name + "-bk"
    vsr_backup_path = os.path.join(LOCAL_LRT_PATH, vsr_backup)
    vsr_path = os.path.join(LOCAL_LRT_PATH, vsr_name)
    remove_file_by_extension(vsr_path, ".gz")
    remove_file_by_extension(vsr_backup_path, ".gz")
    my_logger, my_logfile = create_custom_logger(vsr_logname, LOG_PATH)
    download_lrt_B_with_logger(vsr_ip, vsr_path, REMOTE_LRT_PATH, my_logger)
    list_B = validate_lrt_B_with_logger(vsr_path, my_logger)
    for lrt in list_B:
        n_lrt = 0
        my_logger.info(f"Working in LRT: {lrt}")
        lrt_0 = os.path.join(vsr_path, lrt)
        lrt_bk = os.path.join(vsr_backup_path, lrt)
        shutil.copyfile(lrt_0, lrt_bk)
        my_logger.info(f"Backup LRT {lrt_0} to {lrt_bk}")
        lrt_1 = gunzip_lrt_with_logger(lrt_0, my_logger)
        n = modify_lrt_sag_with_logger(lrt_1, TCONTEXT, FROM_SAG, TO_SAG, my_logger)
        if n:
            lrt_2 = gzip_lrt_with_logger(lrt_1, my_logger)
            my_logger.info(f"Process completed for LRT {lrt_2}\n")
            n_lrt += 1
        else:
            os.remove(lrt_1)
    upload_lrt_B_with_logger(vsr_ip, vsr_path, REMOTE_LRT_PATH, my_logger)
    service = service_account_login()
    EMAIL_SUBJECT = f"Modification in B LRT finished - {vsr_name}"
    EMAIL_CONTENT = f"Hello {EMAIL_TO.split('@')[0]}\nThe replacement from {FROM_SAG} to {TO_SAG} is completed. In total has been modified {n_lrt} LRTs.\nPlease check the logfile attached.\nLGHR"
    HTML_CONTENT = f"<html><body style='font-family:calibri'><p>Hello {EMAIL_TO.split('@')[0]}</p><p>The replacement from {FROM_SAG} to {TO_SAG} is completed. In total has been modified {n_lrt} LRTs.</p><p>Please check the logfile attached.</p><p>LGHR</p></body></html>"
    message = create_message_html_with_attachment(
        EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT, HTML_CONTENT, my_logfile
    )
    sent = send_message(service, "me", message)
    send_telegram_message(
        f"Task Completed:\nModification in B LRT finished - {vsr_name}\nCheck your mailbox"
    )
