from django.urls import path
from . import views

urlpatterns = [
    path('changes/', views.significant_changes, name='significant_changes'),
]
