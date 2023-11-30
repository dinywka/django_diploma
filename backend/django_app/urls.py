from django.urls import path
from . import views
from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView, ProductListView


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

    path('vacancy/', views.vacancy, name='vacancy'),
    path('vacancy/list/', views.vacancy_list, name='vacancy_list'),
    path('vacancy/detail/<str:pk>/', views.vacancy_detail, name='vacancy_detail'),
    path("vacancy/delete/<str:pk>/", views.vacancy_delete, name="vacancy_delete"),
    path("vacancy/update/<str:pk>/", views.vacancy_update, name="vacancy_update"),

    path('resume/', views.resume, name='resume'),
    path('resume/list/', views.resume_list, name='resume_list'),
    path('resume/detail/<str:pk>/', views.resume_detail, name='resume_detail'),
    path('add_hr_rating/<str:pk>/', views.add_hr_rating, name='add_hr_rating'),
    path('resume/<int:resume_id>/download/', views.download_resume, name='download_resume'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),

    path('send_email/', views.send_email, name='send_email'),

    path('api/', views.api, name='api'),

    path('api/products/', ProductListView.as_view(), name='product-list'),

    path('react-page/', views.react_page, name='react_page'),

    # TODO:needs to be the last!!!
    path("rooms/", views.rooms, name="rooms"),
    path("<slug:slug>/", views.room, name="room"),
    path('rooms/create', views.create_room, name="create_room")


]