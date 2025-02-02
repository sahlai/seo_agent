from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_cors import CORS
from dotenv import load_dotenv  # إضافة هذا السطر
load_dotenv() 
app = Flask(__name__)
CORS(app, resources={
    "/webhook": {
        "methods": ["POST"],
        "allow_headers": ["Content-Type"],
        "origins": "*"
    }
})
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'sites.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# استيراد الكلاسات من __init__.py في مجلد models
from app.models import Site, SiteProfile, Category, Tag, ArticleRequest

# استيراد المسارات
from app.routes import sites



# استيراد المسارات
from app.routes import sites
