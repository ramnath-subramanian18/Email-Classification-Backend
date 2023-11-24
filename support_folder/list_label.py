import imaplib
import email
def list_label(email,password):
    print('into this')
# Set your IMAP server and login details
    # email='nikhilesh5475@gmail.com'
    # password='rjoonotrdhtkbcsu'
    IMAP_SERVER = 'imap.gmail.com'
    # Connect to the IMAP server
    with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
        # Log in
        mail.login(email, password)

        # Get the list of labels (mailboxes)
        response, mailbox_list = mail.list()
        
        # Loop through the mailbox list and extract labels
        labels = []
        for mailbox in mailbox_list:
            # The mailbox list response has the format: 'flags delimiter mailbox_name'
            parts = mailbox.decode('utf-8').split(' ')
            label = parts[-1]  # The last part is the label name
            labels.append(label)
        print(labels)
        return labels

        # print("Labels:")
        # for label in labels:
        #     print(label)
