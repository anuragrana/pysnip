from django.urls import path
from snip import views

app_name = "snip"
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'home/', views.index, name='home'),
    path(r'archive/', views.archive, name='archive'),
    path(r'snippet/<int:snippet_id>/', views.get_snippet, name='snippet'),
    path(r'download/text/<int:snippet_id>/', views.download_code_as_file, name='download_code_as_file'),
    path(r'download/image/<int:snippet_id>/', views.download_code_as_image, name='download_code_as_image'),

]
