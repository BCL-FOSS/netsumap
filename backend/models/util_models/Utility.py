import os,os.path
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import requests
from os import system

class Utility:

    def __init__(self) -> None:
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


    def make_request(self, ubiquipy=None, url='', cmd='', payload={'':''}):

        if payload and ubiquipy.auth_check == False:
            print('Empty payload')
            headers={'':''}

        elif not payload and ubiquipy.auth_check == True:
            headers={
                        'Content-Type':'application/json',
                        'Cookie':ubiquipy.token
                    }     
                
        else:
            print('Empty payload')
            headers={'Cookie':ubiquipy.token}
            
        try:

            match cmd.strip():
                case 'g':
                    response = requests.get(url, json=payload, verify=True, headers=headers)
                case 'p':
                    #header={
                    #    'Content-Type':'application/json',
                    #    'Cookie':self.token
                    #}
                    response = requests.post(url, json=payload, verify=True, headers=headers)
                case 'e':
                    response = requests.put(url, json=payload, verify=True, headers=headers)
                case _:
                    system('clear')
                    print('choose an available requests option.')
                    return None

            if response.status_code == 200:
                response.close()
                return response
            else:
                print(response.status_code)
                response.close()
                exit()

        except Exception as e:
            response.close()
            return(print("Error occurred during authentication:", str(e), '\n','Status Code: ', response.status_code))

    
    async def make_async_request(self, url='', payload={}, headers={}, cmd=''):
    
        async with self.ubiquipy_client_session as session:
            try:
                match cmd.strip():
                    case 'g':
                        async with session.get(url=url, json=payload, headers=headers) as response:
                            if response.status == 200:
                                response_data = await response.json()
                                self.auth_check = True
                                response.close()
                                session.close()
                                return {"Message": "Success", "Data": response_data}
                    case 'p':
                        async with session.post(url=url, json=payload, headers=headers) as response:
                            if response.status == 200:
                                response_data = await response.json()
                                self.auth_check = True
                                response.close()
                                session.close()
                                return {"Message": "Success", "Data": response_data}
                    case 'e':
                        async with session.put(url=url, json=payload, headers=headers) as response:
                            if response.status == 200:
                                response_data = await response.json()
                                self.auth_check = True
                                response.close()
                                session.close()
                                return {"Message": "Success", "Data": response_data}
                    case _:
                        system('clear')
                        return {"Message":"Choose a request cmd"}
               
            except aiohttp.ClientError as e:
                return {"error": str(e), "status_code": 500}