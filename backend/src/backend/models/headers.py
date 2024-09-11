if not payload and self.auth_check == False:
            print('Authentication Payload')
            headers={'':''}

        elif not payload and self.auth_check == True:
            headers={
                        'Content-Type':'application/json',
                        'Cookie':self.token
                    }     
                
        else:
            print('Empty payload')
            headers={'Cookie':self.token}