from django.contrib import admin
from django.urls import path, include
from nomy import views as project_Nomy

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', project_Nomy.home, name='home'),
    path('about/', project_Nomy.about, name='about'),
    path('login/', project_Nomy.loginPage, name='login'),
    path('register/', project_Nomy.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('map/', project_Nomy.map, name='map'),
    path('logout/', project_Nomy.logoutUser, name='logout'),
    path('restaurant/', include('restaurant.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)