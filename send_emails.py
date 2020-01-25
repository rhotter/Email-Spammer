from sheets_helpers import get_processed_data
from email_helpers import send_message
from load_parameters import parameters

def main():
    MY_EMAIL = 'mcgillneurotech@gmail.com'
    email_recipients = get_processed_data()
    EMAIL_PLAIN_FILE_NAME = 'email.txt'
    EMAIL_HTML_FILE_NAME = 'email.html'
    
    with open(EMAIL_HTML_FILE_NAME, 'r') as f:
        message_template_html = f.read()
    with open(EMAIL_PLAIN_FILE_NAME, 'r') as f:
        message_template_plain = f.read()
    
    for person in email_recipients[0:1]:
        to = person['email']
        subject = parameters["email subject"]
        msg_html = message_template_html.replace('<NAME>', person['first name'])
        msg_plain = message_template_plain.replace('<NAME>', person['first name'])
        send_message(MY_EMAIL, to, subject, msg_html, msg_plain)
    
if __name__ == '__main__':
    main()