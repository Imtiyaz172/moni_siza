
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('list/<str:class_name>/',views.classsubject),
    path('course/<str:class_name>/',views.course),
    path('list/<str:class_name>/<str:sub_name>/',views.subjectquestion),
    
    path('Practices/<str:classes_name>/<str:sub_name>/<str:chapter_name>/',views.practices),
    path('Written/<str:classes_name>/<str:sub_name>/<str:chapter_name>/<str:type_name>/<int:id>/',views.written),
    path('Video/<str:classes_name>/<str:sub_name>/<str:chapter_name>/',views.video),

    path('contact/',views.contact, name="contact"),
    path('about/',views.about, name="contact"),

    

]
