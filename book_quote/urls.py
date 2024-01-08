from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.homepage, name="homepage"),
    re_path(r'^select2/', include('django_select2.urls')),
    re_path(r'^quotes/', include('quotes.urls')),
    re_path(r'^accounts/', include('accounts.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)