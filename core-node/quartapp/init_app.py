from quart import Quart
import nest_asyncio
import os
import secrets
from models.util.RedisDB import RedisDB
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin
from models.auth_db.AuthDB import AuthDB
from mongoengine import Document
from mongoengine.fields import (
    BinaryField,
    BooleanField,
    DateTimeField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

# Create folder for uploaded PCAP CSVs 
if os.path.isdir(os.path.join(os.path.dirname(__file__), 'Uploads')) is False:
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Uploads'))
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))
else:
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Uploads'))

# Initialize Quart App
app = Quart(__name__)
app.config.from_object("config")

class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)
    permissions = ListField(required=False)
    meta = {"db_alias": app.config['MONGO_DB_NAME']}   

class User(Document, UserMixin):
    email = StringField(max_length=255, unique=True)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    fs_uniquifier = StringField(max_length=64, unique=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
    meta = {"db_alias": app.config['MONGO_DB_NAME']}

# Configure SECRET_KEY and SECURITY_PASSWORD_SALT for secure authentication workflow
if os.environ.get('SECRET_KEY') is None:
   os.environ['SECRET_KEY'] = secrets.token_urlsafe()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if os.environ.get("SECURITY_PASSWORD_SALT") is None:
    os.environ['SECURITY_PASSWORD_SALT'] = secrets.SystemRandom().getrandbits(128)

app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT")

# Configure Authentication Forms
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login_user.html'        # Custom login template
app.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'security/register_user.html'  # Custom registration template
app.config['SECURITY_POST_LOGIN_VIEW'] = '/dashboard'            # Redirect to dashboard on login
app.config['SECURITY_POST_REGISTER_VIEW'] = '/dashboard' 
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/' 
app.config['SECURITY_LOGOUT_METHODS'] = 'POST' 
app.config['SECURITY_REGISTERABLE'] = 'True' 

# Connect to Redis DB
app.config['DB_CONN'] = RedisDB(hostname=app.config['REDIS_DB'], port=app.config['REDIS_DB_PORT'])

if app.config['DB_CONN'] is None:
    print('Verify Redis DB is installed and/or running. Ctrl + C to close netsumap', flush=True) 
    exit()
else:
    print("Redis DB Connected", flush=True)

# Set email validator setting for Flask-Security
app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}

# Connect to MongoDB (Auth Datastore)
db_init = AuthDB()
db = db_init.db_connection(db_name=app.config['MONGO_DB_NAME'], host=app.config['MONGO_DB_NAME'])

if db is None:
    print("verify mongo db is running. Ctrl + C to close netsumap", flush=True)
    exit()
else:
    print("MongoDB Connected", flush=True)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

if app.config['SECURITY'] is None:
    app.config['SECURITY'] = security

app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADER'] = 'application/json'
nest_asyncio.apply()





    
