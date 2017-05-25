from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from dashboard.views import dashboardView, documentoView, portafolioView, googleImport, upLoad, notificationsView
import notifications.urls
from .views import SignupView

urlpatterns = [
    # Include URLS
    url(r'', include('social_django.urls', namespace='social')),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^notifications/", include('notifications.urls', namespace='notifications')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r"^restapi/", include('api.urls')),
    # Static URLS
    url(r"^$", TemplateView.as_view(template_name="homepage.html"),
        name="home"),
    url(r"^login/", TemplateView.as_view(template_name="login.html"), name="login"),
    url(r"^dashboard2/", TemplateView.as_view(template_name="dashboard_v2.html"), name="dashboard2"),
    url(r"^signup/", TemplateView.as_view(template_name="signup.html"), name="signup"),
    url(r"^notifications/(?P<pk>[-\w]+)$", notificationsView.as_view(), name='user_notifications'),
    url(r"^account/signup/$", SignupView.as_view(), name='account_signup'),
    url(r"^googleimp/", googleImport, name="googleImport"),
    url(r"^upload/", upLoad, name="upload"),
    url(r"^portafolios/(?P<pk>[-\w]+)$", portafolioView.as_view(),
        name="portafolios"),
    url(r"^dashboard/(?P<pk>[-\w]+)/(?P<ruc>[0-9]+)/$",
        dashboardView.as_view(), name="user_dashboard"),
    url(r"^documentos/(?P<pk>[-\w]+)/(?P<ruc>[0-9]+)/$",
        documentoView.as_view(), name="user_documentos")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
