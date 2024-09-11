import os,os.path
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from util_models.PDF import PDF

import requests
from os import system


class Utility:

    def __init__(self) -> None:
        pdf = PDF()
        pass

    def send_email(self, subject='', body='', sender='', recipients=[], password='', file_name=''):

        with open(file_name, "rb") as attachment:
            # Add the attachment to the message
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= '{file_name}'",
        )

        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender

        message['To'] = ', '.join(recipients)
        html_part = MIMEText(body)
        message.attach(html_part)
        message.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, message.as_string())

    def generate_pdf(self, title='', author='',output_file_name='', chapters=[]):
        chap_num = 0
        
        try:
            self.pdf.set_title(title)
            self.pdf.set_author(author)
            for chapter in chapters:
                chap_num+=1
                self.pdf.print_chapter(chap_num, chapter['name'], json.dumps(chapter))
            self.pdf.output(output_file_name)
        except Exception as e:
                print(e)
        else:
                print('PDF Report Creation Complete')


    