# app/models/category.py

from app import db

# =========================
# جداول وسيطة (Association Tables)
# =========================

# ربط موقع بتصنيف (many-to-many)
site_categories = db.Table(
    'site_categories',
    db.Column('site_id', db.Integer, db.ForeignKey('site.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

# ربط تصنيف بوسم (many-to-many)
category_tags = db.Table(
    'category_tags',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


# =========================
# موديل Category
# =========================
class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    slug = db.Column(db.String(100))
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # علاقة التصنيف الأب مع تصنيفاته الفرعية
    parent = db.relationship(
        'Category',
        remote_side=[id],
        backref=db.backref('children', lazy='dynamic')
    )

    # علاقة كثير لكثير بين Category و Site عبر الجدول الوسيط site_categories
    sites = db.relationship(
        'Site',
        secondary=site_categories,
        )
    

    # علاقة كثير لكثير بين Category و Tag عبر الجدول الوسيط category_tags
    tags = db.relationship(
        'Tag',
        secondary=category_tags,
        backref=db.backref('categories', lazy='dynamic')
    )

    def __repr__(self):
        return f'<Category {self.name}>'
