from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.homepage,name="homepage"),
    path('contact/',views.contactview, name='contact'),
    path('print/', views.print, name='print'),
     path('register/', views.register_view, name='register'),
     path('pdf/<str:file_name>/', views.view_pdf, name='view_pdf'),
      path('student/', views.user_details, name='user_details'),
        path('paste/<int:paste_id>/', views.show_paste, name='show_paste'),
        path('create/', views.create_paste, name='single_paste'),
]
