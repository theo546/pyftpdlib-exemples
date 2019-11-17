# Permissions

Every letter is used to indicate that the access rights the current FTP user has over the following specific actions are granted.  
The available permissions are the following listed below:

Read permissions:

    "e" = change directory (CWD, CDUP commands)
    "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
    "r" = retrieve file from the server (RETR command)

Write permissions:

    "a" = append data to an existing file (APPE command)
    "d" = delete file or directory (DELE, RMD commands)
    "f" = rename file or directory (RNFR, RNTO commands)
    "m" = create directory (MKD command)
    "w" = store a file to the server (STOR, STOU commands)
    "M" = change file mode / permission (SITE CHMOD command)
    "T" = change file modification time (SITE MFMT command)

Source: https://pyftpdlib.readthedocs.io/en/latest/api.html#users