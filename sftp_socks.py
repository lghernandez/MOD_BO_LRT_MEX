import paramiko, socks, logging, os
from constants import USERNAME, PASSWORD


def create_sftp_connection(host, myuser=USERNAME, mypassword=PASSWORD):
    sock = socks.socksocket()

    sock.set_proxy(
        proxy_type=socks.SOCKS5,
        addr="127.0.0.1",
        port=1500,
    )

    sock.connect((host, 22))

    transport = paramiko.Transport(sock)
    transport.connect(username=myuser, password=mypassword)
    sftp_conn = paramiko.SFTPClient.from_transport(transport)
    return sftp_conn, transport


def download_lrt_B(host, l_path, r_path):
    mysftp, mytransport = create_sftp_connection(host)
    mysftp.chdir(r_path)
    lrt_list = mysftp.listdir()
    for lrt in lrt_list:
        if lrt.startswith("B") and lrt.endswith(".gz"):
            r_file = r_path + "/" + lrt
            l_file = l_path + "\\" + lrt
            mysftp.get(r_file, l_file)
            logging.info("Successfully downloaded LRT: {}".format(lrt))
            print("Successfully downloaded LRT: {}".format(lrt))
    mysftp.close()
    mytransport.close()


def download_lrt_all(host, l_path, r_path):
    mysftp, mytransport = create_sftp_connection(host)
    mysftp.chdir(r_path)
    lrt_list = mysftp.listdir()
    for lrt in lrt_list:
        if lrt.endswith(".gz"):
            r_file = r_path + "/" + lrt
            l_file = l_path + "\\" + lrt
            mysftp.get(r_file, l_file)
            logging.info("Successfully downloaded LRT: {}".format(lrt))
            print("Successfully downloaded LRT: {}".format(lrt))
    mysftp.close()
    mytransport.close()


def upload_lrt_B(host, l_path, r_path):
    mysftp, mytransport = create_sftp_connection(host)
    mysftp.chdir(r_path)
    lrt_list = os.listdir(path=l_path)
    for lrt in lrt_list:
        if lrt.startswith("B") and lrt.endswith(".gz"):
            r_file = r_path + "/" + lrt
            l_file = l_path + "\\" + lrt
            mysftp.put(l_file, r_file)
            logging.info("Successfully uploaded LRT: {}".format(lrt))
            print("Successfully uploaded LRT: {}".format(lrt))
    mysftp.close()
    mytransport.close()
