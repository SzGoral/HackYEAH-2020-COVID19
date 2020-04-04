from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='retina-home'),
    path('about/', views.about, name='retina-about'),
    path('exp/<int:pk>/', views.create_exp_view, name='exp_with_pk'),
    # path('<int:pk>/', views.DataUpdateView.as_view(), name='data_change'),
    path('ajax/load-pxmy/', views.load_px_my, name='ajax_load_pxmy'),
    path('ajax/load-dataxxx/', views.load_dataxxx, name='ajax_load_dataxxx'),
    path('ajax/load-pattern/', views.load_pattern_file, name='ajax_load_pattern'),
    path('ajax/load-pattern-number/', views.load_pattern_number, name='ajax_load_pattern_number'),
    path('ajax/plot-png/', views.get_plot, name='ajax_get_plot'),

    path('ajax/plot-pattern-png/', views.get_pattern_plot, name='ajax_get_pattern_plot'),

    path('ajax/movies-pattern/', views.movie_for_pattern, name='ajax_load_movie_for_pattern'),
    path('ajax/movies/', views.movie_numbers, name='ajax_load_movie_number'),

]
