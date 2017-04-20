from dashboard.views import dashboardView, documentoView, portafolioView, googleImport
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from .views import SignupView

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"),
        name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/signup/$", SignupView.as_view(), name='account_signup'),
    url(r"^account/", include("account.urls")),
    url(r"^googleimp/", googleImport, name="googleImport"),
    url(r"^portfolios/(?P<pk>[-\w]+)$", portafolioView.as_view(),
        name="portafolios"),
    url(r"^dashboard/(?P<pk>[-\w]+)/(?P<ruc>[0-9]+)/$",
        dashboardView.as_view(), name="user_dashboard"),
    url(r"^documentos/(?P<pk>[-\w]+)/(?P<ruc>[0-9]+)/$",
        documentoView.as_view(), name="user_documentos"),
    url(r'', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
