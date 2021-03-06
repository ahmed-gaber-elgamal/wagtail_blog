from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from .views import profile_view
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from search import views as search_views
from .api import api_router
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls
# from pinax.badges.urls import urls

urlpatterns = [
    path(r'comments/', include('django_comments.urls')),
    # url(r'^captcha/', include('captcha.urls')),
    url(r'^tellme/', include("tellme.urls")),

    url(r'^admin/autocomplete/', include(autocomplete_admin_urls)),

    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^api/v2/',api_router.urls ),
    url(r'^sitemap.xml$', sitemap),
    url(r'^account/', include('allauth.urls')),
    path(r'account/profile/', profile_view,  name='account_profile'),
    url(r'', include(wagtail_urls)),


    # url(r"^badges/", include("pinax.badges.urls", namespace="pinax_badges")),



]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
]
