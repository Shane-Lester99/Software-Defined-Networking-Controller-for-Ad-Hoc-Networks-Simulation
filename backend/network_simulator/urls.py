from django.urls import path

from . import views

urlpatterns = [
    path("init_sim/<str:base_station_list>/<int:channel_amount>", views.init_sim),
    path("route_data/<str:source>/<str:dest>", views.route_data),
    path("get_reachable_nodes/<str:source_node>", views.get_reachable_nodes),
    path("reset/", views.reset_graph),
    path("collect_stats/", views.collect_stats),
    path("run_many_simulations/", views.run_many_simulations)
]