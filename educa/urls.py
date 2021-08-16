"""educa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from courses.views import CourseListView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('accounts/login/', auth_view.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', auth_view.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),
    path('students/', include('students.urls')),
    path('articles/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('', CourseListView.as_view(), name='course_list'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
