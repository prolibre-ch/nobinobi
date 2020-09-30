from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from nobinobi_child import urls as nobinobi_child_urls
from nobinobi_core import urls as nobinobi_core_urls
from nobinobi_daily_follow_up import urls as nobinobi_daily_follow_up_urls
from nobinobi_staff import urls as nobinobi_staff_urls
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include(nobinobi_core_urls, namespace="nobinobi_core")),
    path('', include(nobinobi_staff_urls, namespace="nobinobi_staff")),
    path('', include(nobinobi_child_urls, namespace="nobinobi_child")),
    path('', include(nobinobi_daily_follow_up_urls, namespace="nobinobi_daily_follow_up")),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

# OTHER URLS
urlpatterns += [
    path('select2/', include('django_select2.urls')),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
