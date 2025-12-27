from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from blogs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('new/', views.post_edit, name='new_post'),  # 新增博文
    path('edit/<int:post_id>/', views.post_edit, name='edit_post'),  # 编辑博文
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
