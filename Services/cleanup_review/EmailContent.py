
class EmailContent:
    def __init__(self):
        self.DL_CONTENT = """
        <p> {} files/folders will be deleted from your Downloads folder soon! </p>

        <p padding-left: 50pt > {} </p>
        """

        self.TRASH_CONTENT = """
        <p> {} files/folders will be deleted from your Trash folder soon! </p>

        <p padding-left: 50pt > {} </p>
        """

        self.EMAIL_CONTENT = """
        <html>
            <body>
                <p> Howdy Blake! </p>

                <p> This email is a notification for files that are close to being deleted in an
                autonomous task. Below contains information on how many files are going to be
                deleted, and what they are. </p>

                {}

                {}
            </body>
        </html>
        """
