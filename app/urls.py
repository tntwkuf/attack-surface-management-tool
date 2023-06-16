from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('start_search', views.start_search, name='start_search'),
    path('total_clear', views.total_clear, name='total_clear'),
    path('relations_clear', views.relations_clear, name='relations_clear'),
    path('module_clear', views.module_clear, name='module_clear'),
    path('module_add', views.module_add, name='module_add'),
    path('progress_clear', views.progress_clear, name='progress_clear'),
    path('export_search_to_excel', views.export_search_to_excel, name='export_search_to_excel'),
    path('known_ips_clear', views.known_ips_clear, name='known_ips_clear'),
    path('import_from_perimetr', views.import_from_perimetr, name='import_from_perimetr'),
    path('domains_clear', views.domains_clear, name='domains_clear'),
    path('keywords_clear', views.keywords_clear, name='keywords_clear'),
    path('ips_clear', views.ips_clear, name='ips_clear'),
    path('base_graph', views.vis_base_graph, name='base_graph'),
    path('relations_graph', views.vis_relations_graph, name='relations_graph'),
]
