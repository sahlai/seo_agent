from flask import render_template, redirect, url_for, request, flash, jsonify
from app import app, db
from app.models import Site, SiteProfile, Category, Tag, ArticleRequest
from app.models.article import ArticleRequest, article_categories
import requests
import os
from os import environ

# الصفحة الرئيسية
@app.route('/')
def index():
    return redirect(url_for('sites_index'))

# عرض قائمة المواقع
@app.route('/sites')
def sites_index():
    sites = Site.query.all()
    return render_template('sites/index.html', sites=sites)

# إضافة موقع جديد
@app.route('/sites/add', methods=['GET', 'POST'])
def add_site():
    if request.method == 'POST':
        site = Site(
            name=request.form['name'],
            url=request.form['url'],
            wp_user=request.form['wp_user'],
            wp_app_password=request.form['wp_app_password']
        )
        db.session.add(site)
        try:
            db.session.commit()
            flash('تم إضافة الموقع بنجاح', 'success')
        except Exception as e:
            db.session.rollback()
            flash('حدث خطأ أثناء إضافة الموقع', 'error')
            print(f"Error: {str(e)}")
        return redirect(url_for('sites_index'))
    return render_template('sites/add.html')

# تعديل موقع
@app.route('/sites/edit/<int:id>', methods=['GET', 'POST'])
def edit_site(id):
    site = Site.query.get_or_404(id)
    if request.method == 'POST':
        site.name = request.form['name']
        site.url = request.form['url']
        site.wp_user = request.form['wp_user']
        site.wp_app_password = request.form['wp_app_password']
        try:
            db.session.commit()
            flash('تم تحديث الموقع بنجاح', 'success')
        except Exception as e:
            db.session.rollback()
            flash('حدث خطأ أثناء تحديث الموقع', 'error')
            print(f"Error: {str(e)}")
        return redirect(url_for('sites_index'))
    return render_template('sites/edit.html', site=site)

# حذف موقع
@app.route('/sites/delete/<int:id>')
def delete_site(id):
    site = Site.query.get_or_404(id)
    try:
        db.session.delete(site)
        db.session.commit()
        flash('تم حذف الموقع بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء حذف الموقع', 'error')
        print(f"Error: {str(e)}")
    return redirect(url_for('sites_index'))

# صفحة الملف التعريفي
@app.route('/sites/profile/<int:id>', methods=['GET', 'POST'])
def site_profile(id):
    site = Site.query.get_or_404(id)
    if request.method == 'POST':
        if not site.profile:
            profile = SiteProfile(site_id=site.id)
            db.session.add(profile)
        else:
            profile = site.profile

        try:
            profile.brand_name = request.form['brand_name']
            profile.niche = request.form['niche']
            profile.language = request.form['language']
            profile.target_age = request.form['target_age']
            profile.target_region = request.form['target_region']
            profile.target_level = request.form['target_level']
            profile.writing_style = request.form['writing_style']
            profile.avg_word_count = int(request.form['avg_word_count'])
            profile.business_type = request.form['business_type']  # التأكد من حفظ حقل business_type
            
            db.session.commit()
            flash('تم تحديث الملف التعريفي بنجاح', 'success')
        except Exception as e:
            db.session.rollback()
            flash('حدث خطأ أثناء تحديث الملف التعريفي', 'error')
            print(f"Error: {str(e)}")
    
    return render_template('sites/profile.html', site=site)


# إدارة التصنيفات
@app.route('/sites/<int:id>/categories')
def site_categories(id):
    site = Site.query.get_or_404(id)
    return render_template('sites/categories.html', site=site)

# إضافة تصنيف
@app.route('/sites/<int:id>/categories/add', methods=['POST'])
def add_category(id):
    site = Site.query.get_or_404(id)
    try:
        category = Category(
            site_id=site.id,
            name=request.form['name'],
            description=request.form.get('description'),
            parent_id=request.form.get('parent_id') if request.form.get('parent_id') else None
        )
        db.session.add(category)
        db.session.commit()
        flash('تم إضافة التصنيف بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء إضافة التصنيف', 'error')
        print(f"Error: {str(e)}")
    return redirect(url_for('site_categories', id=id))

# جلب تصنيف للتعديل
@app.route('/sites/<int:id>/categories/<int:category_id>/get')
def get_category(id, category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'parent_id': category.parent_id
    })

# تعديل تصنيف
@app.route('/sites/<int:id>/categories/<int:category_id>/edit', methods=['POST'])
def edit_category(id, category_id):
    category = Category.query.get_or_404(category_id)
    try:
        category.name = request.form['name']
        category.description = request.form.get('description')
        category.parent_id = request.form.get('parent_id') if request.form.get('parent_id') else None
        db.session.commit()
        flash('تم تحديث التصنيف بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء تحديث التصنيف', 'error')
        print(f"Error: {str(e)}")
    return redirect(url_for('site_categories', id=id))

# حذف تصنيف
@app.route('/sites/<int:id>/categories/<int:category_id>/delete')
def delete_category(id, category_id):
    category = Category.query.get_or_404(category_id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash('تم حذف التصنيف بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء حذف التصنيف', 'error')
        print(f"Error: {str(e)}")
    return redirect(url_for('site_categories', id=id))

# جلب وسوم التصنيف
@app.route('/sites/<int:id>/categories/<int:category_id>/tags/get')
def get_category_tags(id, category_id):
    category = Category.query.get_or_404(category_id)
    tags = [{'id': tag.id, 'name': tag.name} for tag in category.tags]
    return jsonify(tags)

# إضافة وسم
@app.route('/sites/<int:id>/categories/<int:category_id>/tags/add', methods=['POST'])
def add_tag(id, category_id):
    site = Site.query.get_or_404(id)
    category = Category.query.get_or_404(category_id)
    
    if category.site_id != site.id:
        flash('خطأ في الصلاحيات', 'error')
        return redirect(url_for('site_categories', id=id))
    
    try:
        tag = Tag(
            site_id=site.id,
            name=request.form['name'],
            slug=request.form['name'].lower().replace(' ', '-')
        )
        category.tags.append(tag)
        db.session.add(tag)
        db.session.commit()
        flash('تم إضافة الوسم بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء إضافة الوسم', 'error')
        print(f"Error: {str(e)}")
        
    return redirect(url_for('site_categories', id=id))

# حذف وسم
@app.route('/sites/<int:id>/categories/<int:category_id>/tags/delete/<int:tag_id>')
def delete_category_tag(id, category_id, tag_id):
    site = Site.query.get_or_404(id)
    category = Category.query.get_or_404(category_id)
    tag = Tag.query.get_or_404(tag_id)
    
    try:
        category.tags.remove(tag)
        if not tag.categories:
            db.session.delete(tag)
        db.session.commit()
        flash('تم حذف الوسم بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash('حدث خطأ أثناء حذف الوسم', 'error')
        print(f"Error: {str(e)}")
    
    return redirect(url_for('site_categories', id=id))

# إضافة مقال جديد
@app.route('/sites/<int:id>/article/add', methods=['GET', 'POST'])
def add_article(id):
    site = Site.query.get_or_404(id)
    if request.method == 'POST':
        article = ArticleRequest(
            site_id=site.id,
            title=request.form['title'],
            content_type=request.form['content_type'],
            main_keyword=request.form['main_keyword'],
            secondary_keywords=request.form['secondary_keywords'],
            article_type=request.form['article_type'],
            word_count=int(request.form['word_count']),
            special_requirements=request.form.get('special_requirements'),
            reference_urls=request.form.get('reference_urls'),
            status='pending'
        )
        
        try:
            db.session.add(article)
            db.session.commit()

            # إضافة التصنيف والتاجز المختارة
            category_id = request.form.get('category_id')
            if category_id:
                category = Category.query.get(int(category_id))
                if category:
                    selected_tags = request.form.getlist('tags[]')
                    
                    for tag_id in selected_tags:
                        db.session.execute(article_categories.insert().values(
                            article_id=article.id,
                            category_id=category.id,
                            tag_id=int(tag_id)
                        ))
                    db.session.commit()
                    
            flash('تم إضافة طلب المقال بنجاح', 'success')
            return redirect(url_for('site_profile', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash('حدث خطأ أثناء إضافة طلب المقال', 'error')
            print(f"Error: {str(e)}")
    
    return render_template('sites/article_request.html', site=site)

###
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    print("تم استلام طلب webhook!")
    try:
        data = request.json
        print("البيانات المستلمة:", data)
        return jsonify({
            "status": "success",
            "message": "تم استلام البيانات بنجاح"
        })
    except Exception as e:
        print(f"حدث خطأ: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

#######

@app.route('/sites/<int:id>/analyze-keywords', methods=['POST'])
def analyze_site_keywords(id):
    print("بدء عملية تحليل الكلمات المفتاحية للموقع:", id)
    
    # نجلب الملف التعريفي مباشرة ونتحقق من وجوده
    profile = SiteProfile.query.filter_by(site_id=id).first()
    
    if not profile:
        print("لم يتم العثور على ملف تعريفي للموقع")
        flash('يجب إكمال الملف التعريفي للموقع أولاً', 'error')
        return redirect(url_for('site_profile', id=id))

    # التحقق من اكتمال البيانات المطلوبة
    required_fields = ['brand_name', 'niche', 'business_type', 'language', 
                      'target_region', 'target_age', 'target_level']
    
    missing_fields = [field for field in required_fields 
                     if not getattr(profile, field)]
    
    if missing_fields:
        flash(f'يرجى إكمال البيانات التالية: {", ".join(missing_fields)}', 'error')
        return redirect(url_for('site_profile', id=id))

    # تجهيز البيانات للإرسال
    site_data = {
        "profile_id": profile.id,  # معرف الملف التعريفي
        "site_id": profile.site_id,  # معرف الموقع (نفس id من العلاقة)
        "site_info": {
            "brand_name": profile.brand_name,
            "niche": profile.niche,
            "business_type": profile.business_type,
            "language": profile.language,
            "target_region": profile.target_region,
            "target_age": profile.target_age,
            "target_level": profile.target_level
        }
    }
    
    print("البيانات التي سيتم إرسالها:", site_data)

    try:
        webhook_url = environ.get('N8N_WEBHOOK_URL')
        print("رابط Webhook:", webhook_url)
        
        response = requests.post(
            webhook_url,
            json=site_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print("استجابة Webhook:", response.status_code, response.text)

        if response.ok:
            flash('تم إرسال بيانات الموقع للتحليل بنجاح', 'success')
        else:
            flash(f'حدث خطأ أثناء إرسال البيانات: {response.text}', 'error')
            
    except Exception as e:
        print("حدث خطأ:", str(e))
        flash(f'حدث خطأ في عملية التحليل: {str(e)}', 'error')

    return redirect(url_for('site_profile', id=id))