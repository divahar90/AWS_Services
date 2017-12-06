from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import boto3

# Send the image as attachment through AWS SES after compare_faces service is called

class SendEmail:

    @staticmethod
    def sendEmail(toList, filename):
        msg = MIMEMultipart()
        msg['Subject'] = 'subject'
        msg['From'] = 'from Id'        

        # what a recipient sees if they don't use an email reader
        msg.preamble = 'Multipart message.\n'

        # the message body
        part = MIMEText("Body of the mail")
        msg.attach(part)

        # the attachment
        imgFile = r'target_img_folder' + '\\' + filename
        part = MIMEApplication(open(imgFile, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename='selfie.jpg')
        msg.attach(part)

        # connect to SES
        session = boto3.Session(aws_access_key_id="",
                                aws_secret_access_key="")
        email = session.client(service_name='ses', region_name='us-east-1')

        # and send the message
        result = email.send_raw_email(RawMessage = { 'Data' : msg.as_string() }
            , Source=msg['From']
            , Destinations=toList)
        print result
        
SendEmail.sendEmail();
