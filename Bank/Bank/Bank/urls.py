from django.contrib import admin
from django.urls import path
from bankapp import views

urlpatterns = [
    path("", views.homePage, name="root"),
    path("admin/", admin.site.urls),
    path("home/", views.homePage, name="home"),
    path("add_new/", views.add_new, name="add_new"),
    path("success/", views.success, name="success"),
    path("balance/", views.balance, name="balance"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transfer/", views.transfer, name="transfer"),
    path("viewall/", views.viewall, name="viewall"),
    path("close_account/", views.close_account, name="close_account"),
    path("about_us/", views.about_us, name="about_us"),
    path("account/<int:pk>/edit/", views.user_update, name="user_update"),
    path("account/<int:pk>/delete/", views.user_delete, name="user_delete"),
]
