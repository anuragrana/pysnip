from django.urls import path
from snip import views

app_name = "snip"
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'home/', views.index, name='home'),
    path(r'archive/', views.archive, name='archive'),
    path(r'snippet/new/', views.add_snippet, name='add_snippet'),
    path(r'snippet/<int:snippet_id>/', views.get_snippet, name='snippet'),
    path(r'snippet/next/<int:snippet_id>/', views.get_next_snippet, name='next_snippet'),
    path(r'snippet/previous/<int:snippet_id>/', views.get_previous_snippet, name='previous_snippet'),
    path(r'snippet/random/<int:snippet_id>/', views.get_random_snippet, name='random_snippet'),
    path(r'download/text/<int:snippet_id>/', views.download_code_as_file, name='download_code_as_file'),
    path(r'download/image/<int:snippet_id>/', views.download_code_as_image, name='download_code_as_image'),
    path(r'author/<str:author_username>/', views.author_page, name='author_page'),
]

urlpatterns += [
    path(r'login/', views.mylogin, name='mylogin'),
    path(r'login/github/', views.login_github, name='login_github'),
    path(r'login/github/callback/', views.login_github_callback, name='login_github_callback'),
    path(r'logout/', views.mylogout, name='mylogout'),
]
