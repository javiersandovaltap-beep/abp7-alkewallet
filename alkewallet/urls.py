from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings  # ← agregá esto

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/',  auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('wallet.urls')),
]

# ✅ Debug Toolbar — solo en desarrollo
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns