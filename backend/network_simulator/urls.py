from django.urls import path

from . import views

urlpatterns = [
    path("init_sim/<str:base_station_list>", views.init_sim),
    path("route_data/<str:source>/<str:dest>", views.route_data),
    path("collect_stats/", views.collect_stats)
]