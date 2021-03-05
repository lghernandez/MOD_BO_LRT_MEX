# MOD_BO_LRT_MEX

Script designed to modify a large number of entries in differents Breakout LRT (Local Routing Tables):
1. Download all the B LRTs from a especific host (VSR_HOST) using SFTP.
2. Gunzip each table.
3. Analyze all the entries in order to find which has the value TCONTEXT and then modify the value FROM_SAG for TO_SAG.
4. Gzip each table.
5. Upload all the B LRTs to the especific host (VSR_HOST) using SFTP.
