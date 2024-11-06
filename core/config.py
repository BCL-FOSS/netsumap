#netsumap Backend Configuration File
################################

# IP or Hostname of the websocket server
WEBSOCKET_ADDRESS='ws://:30000/ws'

# Path to IP Classification Keras Model
MODEL='/home/appadmin/ai-threat-mgmt/malicious_ip_multiclass_classification_model.keras'

# Redis DB Connection Information
REDIS_DB="localhost"
REDIS_DB_PORT=6379
REDIS_USER=""
REDIS_PASSWORD=""

# Generate secret key for encryption
SECRET_KEY = ""

