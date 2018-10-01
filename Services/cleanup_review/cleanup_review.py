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

print("\t- Found {} downloads and {} trash files.".format(num_downloads, num_trash))

if num_downloads is not '0':
    print("\t- Collecting downloads...", end='')
    downloads_files = sys.argv[DL_FILES]
    downloads_list = downloads_files.split("\n")
    downloads_files = "<br>".join(downloads_list)
    download_content = email_content.DL_CONTENT.format(num_downloads, downloads_files)
    print("complete.")
else:
    download_content = ""

if num_trash is not '0':
    print("\t- Collecting trash...", end='')
    trash_files = sys.argv[TRASH_FILES]
    trash_list = trash_files.split("\n")
    trash_files = "<br>".join(trash_list)
    trash_content = email_content.TRASH_CONTENT.format(num_trash, trash_files)
    print("complete.")
else:
    trash_content = ""

if num_downloads is not '0' or num_trash is not '0':
    print("\t- Generating email...")
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
        print("\t- Complete.")
    except Exception as e:
        print("\t- Email failed; try again later.")
        print(str(e))
