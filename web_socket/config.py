#Application configuration File
################################
#Secret key that will be used by Flask for securely signing the session cookie
# and can be used for other security related needs
SECRET_KEY = 'SECRET_KEY'
#######################################
#Minimum Number Of Tasks To Generate
MIN_NBR_TASKS = 1
#Maximum Number Of Tasks To Generate
MAX_NBR_TASKS = 100
#Time to wait when producing tasks
WAIT_TIME = 1
#Webhook endpoint Mapping to the listener
WEBHOOK_RECEIVER_URL = 'http://45.32.199.153:5000/consumetasks'
#######################################
#Map to the REDIS Server Port
BROKER_URL = 'redis://localhost:6379'
#######################################
MAX_CONTENT_LENGTH = 16 * 1000 * 1000