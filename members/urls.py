from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.members, name='members'),
# ]


urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('api/heatmap/', views.heatmap_api, name='heatmap_api'),
]
