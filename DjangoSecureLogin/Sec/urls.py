from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import signup
from.views import login_view, verify_code,dashboard,custom_logout,landingpage
from .views import CustomPasswordResetCompleteView
from django.contrib.auth import views as auth_views
from django.urls import path
from DjangoSecureLogin import settings
app_name='Sec'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view,name='login'),
    path('verify-code/<str:username>/', verify_code, name='verify_code'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='myapp_logout'),
    path('logout/',custom_logout,name='CustomLogout'),
    path('home/',landingpage,name='landingpage'),
    
]