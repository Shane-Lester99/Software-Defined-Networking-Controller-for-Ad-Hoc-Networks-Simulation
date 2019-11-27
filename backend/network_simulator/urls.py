from django.urls import path

from . import views

urlpatterns = [
    path('init_sim/', views.init_sim),
    path('route_data/', views.route_data),
    path('collect_stats/', views.collect_stats)
    
]