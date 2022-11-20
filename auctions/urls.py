from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("activeauction", views.activeauction, name="activeauction"),
    path("createauction", views.createauction, name="createauction"),
    path("viewauction/<int:product_id>", views.viewauction, name="viewauction"),
    path("categories", views.categories, name="categories"),
    path("additional_info/<int:product_id>", views.additional_info, name="additional_info"),
    path("addtowatchlist/<int:product_id>",views.addtowatchlist, name="addtowatchlist"),
    path("addcomment/<int:product_id>", views.addcomment, name="addcomment"),
    path("category/<str:categ>", views.category, name="category"),
    path("activeauction/searching", views.searching, name="searching"),
    path("closebid/<int:product_id>", views.closebid, name="closebid"),
    path("activeauction/<str:fil_product>", views.filter_product, name="filter_product"),
    path("closedauction", views.closedauction, name="closedauction")
]
