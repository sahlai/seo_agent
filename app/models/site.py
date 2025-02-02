from app import db
from datetime import datetime

class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    wp_user = db.Column(db.String(50), nullable=False)
    wp_app_password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # العلاقات
    profile = db.relationship('SiteProfile', backref='site', uselist=False)
    categories = db.relationship('Category', backref='site')
    tags = db.relationship('Tag', backref='site')
    article_requests = db.relationship('ArticleRequest', backref='site')

    def __repr__(self):
        return f"<Site id={self.id} name={self.name}>"
