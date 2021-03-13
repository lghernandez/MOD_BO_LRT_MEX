from constants import (
    REMOTE_LRT_PATH,
    LOG_PATH,
    VALIDATE_LRT_PATH,
    EMAIL_FROM,
    EMAIL_TO,
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
from email_notification import (
    service_account_login,
    create_message_html_with_attachment,
    send_message,
)
import os

for vsr_name, vsr_ip in VSRS.items():
    vsr_path = os.path.join(VALIDATE_LRT_PATH, vsr_name)
    remove_file_by_extension(vsr_path, ".xml")
    my_logger, my_logfile = create_custom_logger(vsr_name, LOG_PATH)
    download_lrt_all_with_logger(vsr_ip, vsr_path, REMOTE_LRT_PATH, my_logger)
    list_LRT = validate_lrt_all(vsr_path, my_logger)
    for lrt in list_LRT:
        lrt_1 = gunzip_lrt(lrt, my_logger)
        if lrt_1 is not None:
            validate_lrt_format(lrt_1, my_logger)
    service = service_account_login()
    EMAIL_SUBJECT = f"Validation LRT finished - {vsr_name}"
    EMAIL_CONTENT = f"Hello {EMAIL_TO.split('@')[0]}\nProcess completed. Please check the logfile attached.\nLGHR"
    HTML_CONTENT = f"<html><body style='font-family:calibri'><p>Hello {EMAIL_TO.split('@')[0]}</p><p>Process completed. Please check the logfile attached.</p><p>LGHR</p></body></html>"
    message = create_message_html_with_attachment(
        EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT, HTML_CONTENT, my_logfile
    )
    sent = send_message(service, "me", message)