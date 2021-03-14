# MOD_BO_LRT_MEX

main.py:
========
Script designed to modify a large number of entries in differents Breakout LRT (Local Routing Tables):
1. Download all the B LRTs from a especific host (VSR_HOST) using SFTP.
2. Gunzip each table.
3. Analyze all the entries in order to find which has the value TCONTEXT and then modify the value FROM_SAG for TO_SAG.
4. Gzip each table.
5. Upload all the B LRTs to the especific host (VSR_HOST) using SFTP.

validate_lrt.py:
================
Script designed to connect to all VSRs and validate the format of all LRTs, then generate a logfile with all the information obtained:
1. Iterate through the dic VSRS and get the VSR hostname & VSR IP, then execute the following task for each element.
2. Remove all the files *.xml from the directory assigned to each VSR.
3. Initiate the loggin for the current task.
4. Conect using SFTP to the VSR and download all the LRTs.
5. Validate that the file ends in *.gz.
6. Gunzip each LRT and return the LRT if the gzip file has the right format, if not return None.
7. If the LRT is OK then validate the format and return the following:
    - If there is a syntax error raise a CRITICAL message.
    - If the syntax is OK but the XML file has not the same schema than the XSD file then raise an ERROR message.
8. Notificate by email with the logfile attached when finish the process in the VSR.