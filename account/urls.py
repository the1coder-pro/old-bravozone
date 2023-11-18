from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path("admin/view/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/<int:user_id>", views.profile, name="user_profile"),
    path("all/employee/", views.all_emploee, name="all_emploee"),
    path("signup/employee", views.register_employee, name="register_employee"),
    path("profile/<int:user_id>/edit", views.edit_profile, name="edit_profile")
]
