# from email.message import Message
# import imaplib
# import csv
# import time

# # Function to read the message template from message.txt
# def read_message_template():
#     with open("message.txt", "r") as file:
#         lines = file.readlines()
#         subject = lines[0].strip()
#         body = ''.join(lines[1:])
#         return subject, body

# # Function to replace variables in the message template with corresponding values from the CSV row
# def customize_message(template, row):
#     placeholders = [f"{{Column {i+1}}}" for i in range(len(row))]
#     for i, placeholder in enumerate(placeholders):
#         template = template.replace(placeholder, row[i])
#     return template

# # Function to read email and password from config.txt
# def read_email_password():
#     with open("config.txt", "r") as file:
#         lines = file.readlines()
#         email = lines[0].strip()
#         password = lines[1].strip()
#     return email, password

# # Connect to Gmail
# with imaplib.IMAP4_SSL(host="imap.gmail.com", port=imaplib.IMAP4_SSL_PORT) as imap_ssl:
#     # Read email and password from config.txt
#     email, password = read_email_password()
#     print(f"Logging into mailbox with email: {email}...")
#     resp_code, response = imap_ssl.login(email, password)

#     # Open input.csv file and iterate through rows
#     # with open("input_2.csv", newline='') as csvfile:
#     with open("input.csv", newline='', encoding='utf-8') as csvfile:

#         reader = csv.reader(csvfile)
#         next(reader)  # Skip header row
#         for row in reader:
#             #time.sleep(1)
#             recipient_email = row[0]  # Recipient email is in the first column
#             if not recipient_email:  # Skip if the cell is empty
#                 continue
            
#             # Read message template and customize it with values from the CSV row
#             subject_template, message_body_template = read_message_template()
#             subject = customize_message(subject_template, row[1:])  # Skip the first column (email)
#             message_body = customize_message(message_body_template, row[1:])  # Skip the first column (email)

#             # Create message
#             message = Message()
#             message["From"] = email
#             message["To"] = recipient_email
#             message["Subject"] = subject
#             message.set_payload(message_body)
#             utf8_message = str(message).encode("utf-8")
            
#             # Send message to Drafts
#             imap_ssl.append("[Gmail]/Drafts", '', imaplib.Time2Internaldate(time.time()), utf8_message)

# print("All messages sent to Drafts.")

####################################################################################################################
# from nicegui import ui

# ui.button("Say Hello", on_click=lambda: ui.notify("Hello, World!"))
# ui.run(title="Hello, World!")
######################################################################################
# from nicegui import ui

# def read_file():
#     with open('message.txt', 'r') as file:
#         print(file.read())

# ui.button("Read File", on_click=read_file)
# ui.run(title="File Reader")
##############################################################################3

# from nicegui import ui

# def read_file(file):
#     with open(file, 'r') as f:
#         print(f.read())

# ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')
# ui.button("Read File", on_click=read_file)

# ui.run(title="File Reader")
######################################################
# from nicegui import ui

# def read_file(content):
#     print(content.decode())

# def on_upload(e):
#     ui.notify(f'Uploaded {e.name}')
#     read_file(e.content)

# ui.upload(on_upload=on_upload).classes('max-w-full')

# ui.run(title="File Reader")
###################################################################################################
#################################################################################################
# from nicegui import events, ui

# with ui.dialog().props('full-width') as dialog:
#     with ui.card():
#         content = ui.markdown()

# # Upload Recipients
# def recipient_upload(e: events.UploadEventArguments):
#     recipient = e.content.read().decode('utf-8')
#     content.set_content(recipient)
#     cont = dialog.open()
#     print(recipient)
    
# ui.label('Upload Recipients as .csv file')
# ui.upload(on_upload=recipient_upload).props('accept=.csv').classes('max-w-full')



# # Upload Message
# def message_upload(e: events.UploadEventArguments):
#     message = e.content.read().decode('utf-8')
#     content.set_content(message)
#     cont = dialog.open()
#     print(message)
    
# ui.label('Upload Draft Message as .txt file')
# ui.upload(on_upload=message_upload).props('accept=.txt').classes('max-w-full')


# # Upload Email & App Password
# def credentials_upload(e: events.UploadEventArguments):
#     credentials = e.content.read().decode('utf-8')
#     content.set_content(credentials)
#     cont = dialog.open()
#     print(credentials)
# ui.label('Upload Email & App Password as .txt file')
# ui.upload(on_upload=credentials_upload).props('accept=.txt').classes('max-w-full')

# #######################################################################################################3
# # Create Draft Function
# ui.button('Create Drafts!', on_click=lambda: ui.notify('Drafts Created Successfully!'))



# ui.run()
#######################################################################################################
#######################################################################################################
from nicegui import events, ui
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import time

recipient = None
message = None
credentials = None

with ui.dialog().props('full-width') as dialog:
    with ui.card():
        content = ui.markdown()

# Upload Recipients
def recipient_upload(e: events.UploadEventArguments):
    global recipient
    recipient = e.content.read().decode('utf-8')
    content.set_content(recipient)
    cont = dialog.open()
    print(recipient)

ui.label('Upload Recipients as .csv file')
ui.upload(on_upload=recipient_upload).props('accept=.csv').classes('max-w-full')

# Upload Message
def message_upload(e: events.UploadEventArguments):
    global message
    message = e.content.read().decode('utf-8')
    content.set_content(message)
    cont = dialog.open()
    print(message)

ui.label('Upload Draft Message as .txt file')
ui.upload(on_upload=message_upload).props('accept=.txt').classes('max-w-full')


# Upload Email & App Password
def credentials_upload(e: events.UploadEventArguments):
    global credentials
    credentials = e.content.read().decode('utf-8')
    content.set_content(credentials)
    cont = dialog.open()
    print(credentials)

ui.label('Upload Email & App Password as .txt file')
ui.upload(on_upload=credentials_upload).props('accept=.txt').classes('max-w-full')


#######################################################################################################
# Create Draft Function
def create_drafts():
    global recipient, message, credentials
    
    # Parse credentials
    user_email, app_password = credentials.strip().split('\n')
    
    # Connect to the IMAP server
    imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
    
    try:
        imap_server.login(user_email, app_password)
    except Exception as e:
        print("Error logging in:", e)
        return
    
    # Split recipient data into rows
    recipient_rows = recipient.strip().split('\n')
    
    # Extract column headers from the first row and strip whitespace characters
    headers = [header.strip() for header in recipient_rows[0].split(',')]
    
    # Iterate through each recipient row (excluding the header row)
    for recipient_row in recipient_rows[1:]:
        # Split recipient row into email address and variables
        row_values = recipient_row.split(',')
        recipient_email = row_values[0]  # First column contains email address
        
        # Create a dictionary to map column headers to values for the recipient
        recipient_data = dict(zip(headers[1:], row_values[1:]))
        
        # Substitute variables in message template for the recipient
        formatted_message = message
        for header, value in recipient_data.items():
            placeholder = f'{{{header}}}'
            formatted_message = formatted_message.replace(placeholder, value)
        
        # Create MIME message
        msg = MIMEMultipart()
        msg['From'] = user_email
        msg['To'] = recipient_email
        msg['Subject'] = formatted_message.split('\n', 1)[0]  # Extract subject from first line of message
        msg.attach(MIMEText(formatted_message, 'plain'))
        
        # Encode message as bytes
        msg_bytes = msg.as_bytes()
        
        try:
            # Create draft for the recipient
            result = imap_server.append('[Gmail]/Drafts', '', imaplib.Time2Internaldate(time.time()), msg_bytes)
            print("Draft created for:", recipient_email)
            print("Result:", result)
        except Exception as e:
            print("Error creating draft for", recipient_email, ":", e)
    
    # Logout from IMAP server
    imap_server.logout()





    print("k")


print(recipient, message, credentials)
ui.button('Create Drafts!', on_click=create_drafts)

ui.run()
