import imaplib
def label_creation(userid,password,label_list):
    def check_label_exists(mail, label_name):
        # List all labels (folders)
        status, folder_list = mail.list()

        if status == 'OK':
            for folder_info in folder_list:
                _, folder_name = folder_info.split(b' "/" ')
                folder_name = folder_name.decode("utf-8").strip('"')

                if folder_name == label_name:
                    return True

        return False

    def create_gmail_label(username, password, label_name):
        # Connect to Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        # Log in to the Gmail account
        mail.login(username, password)

        label_name = label_name.encode('utf-8')

        if not check_label_exists(mail, label_name):
            # Create the label if it doesn't exist
            status, response = mail.create(label_name)

            if status == 'OK':
                print(f"Label '{label_name.decode('utf-8')}' created successfully.")
            else:
                print("Label creation failed.")
        else:
            print(f"Label '{label_name.decode('utf-8')}' already exists. Skipping label creation.")

        # Close the connection
        mail.logout()

    # Replace these with your Gmail credentials and the label name you want to create
    gmail_username = userid
    gmail_password = password
    # new_label_name = "Label12345"
    # label=['hello','hello123','helloo1233']
    for i in label_list:
        create_gmail_label(gmail_username, gmail_password, i)
