from app import db, app
import os
from sqlalchemy import inspect

def init_db():
    if os.path.exists('instance/sites.db'):
        os.remove('instance/sites.db')
        print("تم حذف قاعدة البيانات القديمة")

    with app.app_context():
        db.create_all()
        print("تم إنشاء قاعدة البيانات الجديدة")

        try:
            # استخدام inspector لعرض الجداول
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print("\nالجداول التي تم إنشاؤها:")
            for table in tables:
                print(f"- {table}")
            
            if len(tables) == 0:
                print("تحذير: لم يتم إنشاء أي جداول!")
        except Exception as e:
            print(f"حدث خطأ: {str(e)}")

if __name__ == '__main__':
    init_db()