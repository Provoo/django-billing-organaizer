from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from dashboard.views import dashboardView, documentoView, homeView, portafolioView, googleImport, upLoad, notificationsView
import notifications.urls
from .views import SignupView

urlpatterns = [
    url(r'', include('social_django.urls', namespace='social')),
    url(r"^$", TemplateView.as_view(template_name="homepage.html"),
        name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^notifications/", include(notifications.urls, namespace='notifications')),
    url(r"^notifications/(?P<pk>[-\w]+)$", notificationsView.as_view(), name='user_notifications'),
    url(r"^account/signup/$", SignupView.as_view(), name='account_signup'),
    url(r"^googleimp/", googleImport, name="googleImport"),
    url(r"^upload/", upLoad, name="upload"),
    url(r"^portfolios/(?P<pk>[-\w]+)$", portafolioView.as_view(),
        name="portafolios"),
    url(r"^dashboard/(?P<pk>[-\w]+)/(?P<ruc>[0-9]+)/$",
        dashboardView.as_view(), name="user_dashboard"),
    url(r"^documentos/(?P<pk>[-\w]+)/(?P<ruc>[0-9]+)/$",
        documentoView.as_view(), name="user_documentos"),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
