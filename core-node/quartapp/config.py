#netsumap Backend Configuration File
################################

# Path to IP Classification Keras Model
MODEL='/home/appadmin/ai-threat-mgmt/malicious_ip_multiclass_classification_model.keras'

# Redis DB Connection Data
REDIS_DB="redis"
REDIS_DB_PORT=6379
REDIS_USER=""
REDIS_PASSWORD=""
DB_CONN=None

# MongoDB Connection Data
MONGO_DB_NAME="mongo"
MONGO_DB_HOST="mongo"
MONGO_DB_PORT=27017

# Generate secret key for encryption
SECRET_KEY = ""

# Flask Security Object
SECURITY = None

