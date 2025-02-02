from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # إنشاء قاعدة البيانات وجداولها أولاً
        
    app.run(host='0.0.0.0', port=5678, debug=True)  # تشغيل السيرفر
   