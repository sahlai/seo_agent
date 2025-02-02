# app/models/__init__.py

from .site import Site
from .site_profile import SiteProfile
from .category import Category
from .tag import Tag
from .article import ArticleRequest


# يمكنك إضافة بقية الموديلات هنا أو تجاهل هذه الطريقة
# إذا أردت التجميع. لا تُعرّف جداول وسيطة هنا.
__all__ = [
    'Site',
    'SiteProfile',
    'Category',
    'Tag',
    'ArticleRequest',
    'SiteCategory'
]
