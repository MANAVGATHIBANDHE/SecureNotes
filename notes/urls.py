# notes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create-note/', views.create_note_view, name='create_note'),
    path('notes/', views.list_notes, name='list_notes'),
    path('notes/<int:pk>/',   views.detail_note,   name='detail_note'),
    path('notes/<int:pk>/edit/',   views.edit_note,   name='edit_note'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
]
