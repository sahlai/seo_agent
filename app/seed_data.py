from app import db
from app.models.business_type import BusinessType

def seed_business_types():
    """
    دالة لإضافة أنواع الأعمال الأساسية في قاعدة البيانات.
    نقوم بإضافة الأنواع الأساسية التي نحتاجها للبداية.
    """
    default_types = [
        {
            "name": "متجر إلكتروني",
            "description": "موقع مخصص لبيع المنتجات عبر الإنترنت"
        },
        {
            "name": "موقع معلوماتي",
            "description": "موقع يقدم محتوى تعليمي ومعلومات مفيدة للزوار"
        },
        {
            "name": "موقع خدمات",
            "description": "موقع يقدم خدمات مختلفة للعملاء"
        },
        {
            "name": "مدونة",
            "description": "موقع يركز على نشر المقالات والمحتوى الدوري"
        }
    ]
    
    # نضيف كل نوع إذا لم يكن موجوداً بالفعل
    for type_data in default_types:
        existing = BusinessType.query.filter_by(name=type_data["name"]).first()
        if not existing:
            new_type = BusinessType(**type_data)
            db.session.add(new_type)
    
    # نحفظ التغييرات في قاعدة البيانات
    try:
        db.session.commit()
        print("تم إضافة أنواع الأعمال الأساسية بنجاح")
    except Exception as e:
        db.session.rollback()
        print(f"حدث خطأ أثناء إضافة أنواع الأعمال: {str(e)}")