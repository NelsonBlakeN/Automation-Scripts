#!/usr/bin/python3
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailUtils import EmailUtils
from EmailContent import EmailContent

DL_QUANTITY     = 1
DL_FILES        = 2
TRASH_QUANTITY  = 3
TRASH_FILES     = 4

downloads_files = None
num_downloads   = sys.argv[DL_QUANTITY]
trash_files     = None
num_trash       = sys.argv[TRASH_QUANTITY]

email_content = EmailContent()

if num_downloads is not 0:
    downloads_files = sys.argv[DL_FILES]
    download_content = email_content.DL_CONTENT.format(num_downloads, downloads_files)
else:
    download_content = ""

if num_trash is not 0:
    trash_files = sys.argv[TRASH_FILES]
    trash_content = email_content.TRASH_CONTENT.format(num_trash, trash_files)
else:
    trash_content = ""

if num_downloads is 0 or num_trash is 0:
    try:
        utils = EmailUtils()
        email = email_content.EMAIL_CONTENT.format(download_content, trash_content)

        msg = MIMEMultipart("alternative", None, [MIMEText(email, 'html')])
        msg['Subject'] = "Cleanup Review"
        msg['From'] = utils.FROM
        msg['TO'] = utils.TO
        server = smtplib.SMTP(utils.SERVER)
        server.ehlo()
        server.starttls()
        server.login(utils.TO, utils.PASSWORD)
        server.sendmail(utils.FROM, utils.TO, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email failed; try again later.")
        print(str(e))
