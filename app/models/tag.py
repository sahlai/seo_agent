from app import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50))

    def __repr__(self):
        return f'<Tag {self.name}>'