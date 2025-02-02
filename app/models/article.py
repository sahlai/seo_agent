# app/models/article.py
from app import db
from datetime import datetime

# انقل الجدول الوسيط من __init__.py إلى هنا:
article_categories = db.Table(
    'article_categories',
    db.Column('article_id', db.Integer, db.ForeignKey('article_request.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)
# إذا لديك جداول وسيطة أخرى مثل article_tags, category_tags
# يمكنك وضعها هنا أيضاً أو في ملف مخصص آخر
# -----------------------------------------------------------

class ArticleRequest(db.Model):
    __tablename__ = 'article_request'  # إضافة اختيارية لضبط اسم الجدول
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))

    content_type = db.Column(db.String(20))  # page/article
    title = db.Column(db.String(200), nullable=False)
    main_keyword = db.Column(db.String(100))
    secondary_keywords = db.Column(db.Text)
    article_type = db.Column(db.String(50))
    word_count = db.Column(db.Integer)
    special_requirements = db.Column(db.Text)
    reference_urls = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    # العلاقات
    # استخدم الجدول الوسيط المُعرف أعلاه
    categories = db.relationship('Category', secondary=article_categories)

    def __repr__(self):
        return f'<ArticleRequest {self.title}>'
