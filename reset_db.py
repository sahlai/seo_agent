# في ملف reset_db.py في المجلد الرئيسي
from app import create_app, db
from app.models.business_type import BusinessType
from app.models.site_profile import SiteProfile

def reset_database():
    app = create_app()
    with app.app_context():
        print("جاري حذف وإعادة إنشاء قاعدة البيانات...")
        db.drop_all()
        db.create_all()
        
        print("إضافة أنواع الأعمال الأساسية...")
        default_types = [
            BusinessType(name="متجر إلكتروني", description="موقع لبيع المنتجات عبر الإنترنت"),
            BusinessType(name="موقع خدمات", description="موقع يقدم خدمات متنوعة"),
            BusinessType(name="موقع معلوماتي", description="موقع يقدم محتوى تعليمي ومعلوماتي"),
            BusinessType(name="مدونة", description="موقع لنشر المقالات والمحتوى")
        ]
        
        for business_type in default_types:
            db.session.add(business_type)
        
        try:
            db.session.commit()
            print("تم إعادة تهيئة قاعدة البيانات بنجاح!")
        except Exception as e:
            db.session.rollback()
            print(f"حدث خطأ: {str(e)}")

if __name__ == "__main__":
    reset_database()