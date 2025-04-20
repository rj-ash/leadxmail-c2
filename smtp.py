# import os
# import time
# import smtplib
# import imaplib
# import email
# from email.mime.text import MIMEText
# from email.utils import formatdate
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# def send_and_capture_emails(test_emails):
#     # Configuration
#     SMTP_SERVER = 'smtp.gmail.com'
#     SMTP_PORT = 587
#     IMAP_SERVER = 'imap.gmail.com'
#     IMAP_PORT = 993
#     USERNAME = os.getenv('SMTP_USERNAME')
#     PASSWORD = os.getenv('SMTP_PASSWORD')
    
#     email_bodies = []
    
#     try:
#         # Phase 1: Send emails
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
#             smtp.starttls()
#             smtp.login(USERNAME, PASSWORD)
            
#             for to_email in test_emails:
#                 msg = MIMEText("This is a test email")
#                 msg['Subject'] = "Test Email"
#                 msg['From'] = USERNAME
#                 msg['To'] = to_email
#                 msg['Date'] = formatdate(localtime=True)
#                 smtp.send_message(msg)
#                 print(f"Sent test email to {to_email}")

#         # Wait for incoming emails
#         print("\nWaiting 60 seconds to capture incoming emails...")
#         start_time = time.time()
#         time.sleep(60)
        
#         # Phase 2: Capture incoming emails
#         with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as imap:
#             imap.login(USERNAME, PASSWORD)
#             imap.select('INBOX')
            
#             # Search for emails received during the waiting period
#             since_time = time.strftime("%d-%b-%Y %H:%M:%S", 
#                                      time.localtime(start_time - 10))
#             _, data = imap.search(None, 
#                                 f'(SINCE "{since_time}")')
            
#             email_ids = data[0].split()
#             print(f"\nFound {len(email_ids)} emails during monitoring period")

#             # Fetch and store email bodies
#             for email_id in email_ids:
#                 _, msg_data = imap.fetch(email_id, '(RFC822)')
#                 email_msg = email.message_from_bytes(msg_data[0][1])
                
#                 body = ""
#                 if email_msg.is_multipart():
#                     for part in email_msg.walk():
#                         content_type = part.get_content_type()
#                         content_disposition = str(part.get("Content-Disposition"))
                        
#                         if "attachment" not in content_disposition:
#                             if content_type in ["text/plain", "text/html"]:
#                                 try:
#                                     body += part.get_payload(decode=True).decode()
#                                 except:
#                                     body += part.get_payload(decode=True).decode('latin-1')
#                 else:
#                     try:
#                         body = email_msg.get_payload(decode=True).decode()
#                     except:
#                         body = email_msg.get_payload(decode=True).decode('latin-1')
                
#                 email_bodies.append({
#                     'subject': email_msg['subject'],
#                     'from': email_msg['from'],
#                     'body': body.strip()
#                 })

#         return email_bodies

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return []

# if __name__ == "__main__":
#     # Example usage
#     test_emails = ["recipient1@example.com", "recipient2@example.com"]
    
#     # Create .env file with:
#     # GMAIL_USERNAME=your@gmail.com
#     # GMAIL_PASSWORD=your-app-password
    
#     print("Starting email test...")
#     captured_emails = send_and_capture_emails(test_emails)
    
#     print("\nCaptured Email Bodies:")
#     for idx, email in enumerate(captured_emails, 1):
#         print(f"\nEmail {idx}:")
#         print(f"From: {email['from']}")
#         print(f"Subject: {email['subject']}")
#         print("Body:")
#         print("-" * 50)
#         print(email['body'])
#         print("-" * 50)