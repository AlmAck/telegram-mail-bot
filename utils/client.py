import logging
import poplib
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from utils.mail import Email
from email.message import EmailMessage


logger = logging.getLogger(__name__)



class EmailClient(object):
    def __init__(self, email_account, passwd):
        self.email_account = email_account
        self.password = passwd
        self.server = self.connect(self)

    @staticmethod
    def connect(self):
        # parse the server's hostname from email account
        pop3_server = 'pop3s.'+self.email_account.split('@')[-1]
        server = poplib.POP3_SSL(pop3_server)
        # display the welcome info received from server,
        # indicating the connection is set up properly
        logger.info(server.getwelcome().decode('utf8'))
        # authenticating
        server.user(self.email_account)
        server.pass_(self.password)
        return server

    def get_mails_list(self):
        _, mails, _ = self.server.list()
        return mails

    def get_mails_count(self):
        mails = self.get_mails_list()
        return len(mails)

    def get_mail_by_index(self, index):
        resp_status, mail_lines, mail_octets = self.server.retr(index)
        return Email(mail_lines)

    def send_mail(self, to_emails, subject, text):
        email_message = EmailMessage()
        email_message.add_header('To', ', '.join(to_emails))
        email_message.add_header('From', self.email_account)
        email_message.add_header('Subject', subject)
        #email_message.add_header('X-Priority', '1')  # Urgency, 1 highest, 5 lowest
        email_message.set_content(text)

        # Connect, authenticate, and send mail
        smtp_server_name = 'smtpauths.'+self.email_account.split('@')[-1]
        smtp_server = SMTP_SSL(smtp_server_name, port=SMTP_SSL_PORT)
        smtp_server.set_debuglevel(1)  # Show SMTP server interactions
        smtp_server.login(self.email_account, self.password)
        smtp_server.sendmail(self.email_account, to_emails, email_message.as_bytes())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            logger.info('exited normally\n')
            self.server.quit()
        else:
            logger.error('raise an exception! ' + str(exc_type))
            self.server.close()
            return False # Propagate



if __name__ == '__main__':
    useraccount = "XXXXX"
    password = "XXXXXX"

    client = EmailClient(useraccount, password)
    num = client.get_mails_count()
    print(num)
    for i in range(1, num):
        print(client.get_mail_by_index(i))
