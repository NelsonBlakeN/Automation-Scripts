#!/usr/bin/python3

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailUtils import FROM, TO, SERVER, PASSWORD
from EmailContent import DL_CONTENT, TRASH_CONTENT, EMAIL_CONTENT

DL_NUM = 1
DL_LIST = 2
TRASH_NUM = 3
TRASH_LIST = 4

downloads = None
num_downloads = sys.argv[DL_NUM]
trash = None
num_trash = sys.argv[TRASH_LIST]

if num_downloads is not 0:
    downloads = sys.argv[DL_LIST]
    DL_CONTENT = DL_CONTENT.format(num_downloads, downloads)
else:
    DL_CONTENT = ""

if sys.argv[TRASH_NUM] is not 0:
    trash = sys.argv[TRASH_LIST]
    TRASH_CONTENT = TRASH_CONTENT.format(num_trash, trash)
else:
    TRASH_CONTENT = ""

if downloads is not None or trash is not None:
    try:
        EMAIL_CONTENT.format(DL_CONTENT, TRASH_CONTENT)

        msg = MIMEMultipart("alternative", None, [MIMEText(EMAIL_CONTENT, 'html')])
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
