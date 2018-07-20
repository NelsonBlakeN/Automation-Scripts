#!/usr/bin/python3

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailUtils import FROM, TO, SERVER, PASSWORD
from EmailContent import EmailContent

DL_QUANTITY     = 1
DL_FILES        = 2
TRASH_QUANTITY  = 3
TRASH_FILES     = 4

downloads_files = None
num_downloads   = sys.argv[DL_QUANTITY]
trash_files     = None
num_trash       = sys.argv[TRASH_QUANTITY]

email_content       = EmailContent()
files_from_download = ""
files_from_trash    = ""
email_text          = ""

if num_downloads is not 0:
    downloads_files = sys.argv[DL_FILES]
    files_from_download = email_content.DL_CONTENT.format(num_downloads, downloads_files)

if num_trash is not 0:
    trash_files = sys.argv[TRASH_FILES]
    files_from_trash = email_content.TRASH_CONTENT.format(num_trash, trash_files)

if downloads_files is not None or trash_files is not None:
    try:
        email_text = email_content.EMAIL_CONTENT.format(files_from_download, files_from_trash)

        print("Email content: " + email_text)

        msg = MIMEMultipart("alternative", None, [MIMEText(email_text, 'html')])
        msg['Subject'] = "Cleanup Review"
        msg['From'] = FROM
        msg['TO'] = TO
        server = smtplib.SMTP(SERVER)
        server.ehlo()
        server.starttls()
        server.login(TO, PASSWORD)
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email failed; try again later.")
        print(str(e))
