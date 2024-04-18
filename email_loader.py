import imaplib
import email
from email.header import decode_header

from email_model import Email


class EmailLoader:
    def __init__(self, imap_server, username, password):
        self.imap_server = imap_server
        self.username = username
        self.password = password

    def load_emails(self, num_emails=10) ->  list[Email]:
        # Connect to the IMAP server
        imapobj = imaplib.IMAP4_SSL(self.imap_server)
        imapobj.login(self.username, self.password)

        # Select the email folder
        imapobj.select('Inbox')

        email_list = []

        # Fetch the most recent 10 email messages
        # Note: here we fetch all and split later, but we could use .search with a BEFORE criteria to
        # get only the emails from the last 24 hours, for example. See https://gist.github.com/martinrusev/6121028
        status, data = imapobj.search(None, 'ALL')
        if data[0]:
            messages = data[0].split()
            if len(messages) > num_emails:
                messages = messages[-num_emails:]
            for num in messages:
                status, msg_data = imapobj.fetch(num, '(RFC822)')
                message = email.message_from_bytes(msg_data[0][1])

                # Extract the sender and subject
                id = message['Message-ID']
                date = message['Date']
                from_addr = message['From']
                to = message['To']

                subject, encoding = decode_header(message['Subject'])[0]
                
                if isinstance(subject, bytes):
                    if encoding:
                        subject = subject.decode(encoding)
                    else:
                        subject = subject.decode('utf-8', errors='replace')
                
                # Initialize a variable to hold the email body
                email_body = None

                # Check if the email is multipart (e.g., text and attachments)
                if message.is_multipart():
                    # Iterate over each part of the email
                    for part in message.walk():
                        content_type = part.get_content_type()
                        content_disposition = part.get("Content-Disposition") if part.get("Content-Disposition") else ''

                        # Look for text parts, but skip attachments
                        if content_type == 'text/plain' and 'attachment' not in content_disposition:
                            # Get the text/plain part
                            email_body = part.get_payload(decode=True).decode()
                            break
                        elif content_type == 'text/html' and 'attachment' not in content_disposition:
                            # Get the text/html part
                            email_body = part.get_payload(decode=True).decode()
                            break
                else:
                    # Email is not multipart
                    content_type = message.get_content_type()
                    if content_type == 'text/plain' or content_type == 'text/html':
                        email_body = message.get_payload(decode=True).decode()
                

                # Check if the email has an attachment
                filename = None
                for part in message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    
                    # Extract filename
                    filename = part.get_filename()


                # Create an Email object
                email_obj = Email(id, date, from_addr, to, subject, email_body, filename)
                email_list.append(email_obj)
        else:
            print("No messages found in the Inbox.")

        # Close the email connection
        imapobj.close()
        imapobj.logout()

        return email_list
