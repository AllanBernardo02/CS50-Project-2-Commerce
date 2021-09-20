
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categ, name="categories"),
    path("categories/<int:cat_id>",views.specific, name='specific'),
    path("watchlist/",views.watchlist, name='watchlist'),
    path("<int:list_id>",views.show_listing, name='listing'), 
    path("add", views.create_listing, name='create_listing'),
    path("My_Listing",views.show_my_listing, name= 'user_listing'),
    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)