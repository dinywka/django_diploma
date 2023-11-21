from django.urls import path
from . import views
from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_f, name='login'),
    path('profile/', views.profile_f, name='profile'),
    path('logout/', views.logout_f, name='logout'),

    path('ideas/', views.ideas, name='ideas'),
    path('ideas/list/', views.ideas_list, name='ideas_list'),
    path('idea/detail/<str:pk>/', views.idea_detail, name='idea_detail'),
    path("idea/delete/<str:pk>/", views.idea_delete, name="idea_delete"),
    path("idea/update/<str:pk>/", views.idea_update, name="idea_update"),
    path("idea/comment/create/<str:pk>/", views.idea_comment_create, name="idea_comment_create"),
    path("idea/rating/<str:pk>/<str:is_like>/", views.idea_rating, name="idea_rating"),
    path('news/', views.news, name="news"),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),

    path('send_email/', views.send_email, name='send_email'),

    # TODO:needs to be the last!!!
    path("rooms/", views.rooms, name="rooms"),
    path("<slug:slug>/", views.room, name="room"),


]