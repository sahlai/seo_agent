from app import db

class SiteProfile(db.Model):
    __tablename__ = 'site_profile'
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), unique=True)
    
    brand_name = db.Column(db.String(100))
    niche = db.Column(db.String(100))
    business_type = db.Column(db.String(50))
    language = db.Column(db.String(50))
    target_age = db.Column(db.String(50))
    target_region = db.Column(db.String(100))
    target_level = db.Column(db.String(50))
    writing_style = db.Column(db.String(50))
    avg_word_count = db.Column(db.Integer)

    def __repr__(self):
        return f"<SiteProfile brand={self.brand_name}>"
