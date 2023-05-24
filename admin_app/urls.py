from django.urls import path
from admin_app import views


urlpatterns = [
    path('user_login/',views.UserLoginView.as_view()),
    path('user_register/',views.UserRegisterView.as_view()),
    path('user_profile/',views.UserProfilesView.as_view()),
    path('user_update/<int:id>/',views.UserUpdateView.as_view()), 
    path('user_logout_views/',views.UserLogoutView.as_view()),
]