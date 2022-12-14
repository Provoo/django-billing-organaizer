from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from dashboard.views import dashboardView, documentoView, portfoliosView, googleImport, upLoad, upLoadManual, notificationsView, registerExpenses, tagsconsult, savetags
import notifications.urls
from wallet.views import walletsView
from .views import SignupView


urlpatterns = [
    # Include URLS
    url(r'', include('social_django.urls', namespace='social')),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/signup/$", SignupView.as_view(), name='account_signup'),
    url(r"^account/", include("account.urls")),
    url(r"^notifications/", include('notifications.urls', namespace='notifications')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r"^restapi/", include('api.urls')),
    # Static URLS
    url(r"^$", TemplateView.as_view(template_name="homepage.html"),
        name="home"),
    url(r"^login/", TemplateView.as_view(template_name="login.html"), name="login"),
    url(r"^inbox/notifications/", notificationsView.as_view(), name='user_notifications'),
    url(r"^googleimp/", googleImport, name="googleImport"),
    url(r"^upload/", upLoad, name="upload"),
    url(r"^uploadmanual/", upLoadManual, name="uploadmanual"),
    url(r"^create_expenses/(?P<ruc>[0-9]+)/$", registerExpenses, name="create_expenses"),
    url(r"^tagsconsult/(?P<ruc>[0-9]+)/$", tagsconsult, name="tagsconsult"),
    url(r"^savetags/(?P<ruc>[0-9]+)/$", savetags, name="savetags"),
    url(r"^portfolios/", portfoliosView.as_view(),
        name="user_portfolios"),
    url(r"^dashboard/(?P<ruc>[0-9]+)/$",
        dashboardView.as_view(), name="user_dashboard"),
    url(r"^documentos/(?P<ruc>[0-9]+)/$",
        documentoView.as_view(), name="user_documentos"),
    url(r"^wallets/", walletsView.as_view(), name="user_wallets")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
