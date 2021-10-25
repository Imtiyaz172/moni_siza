
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('prv-ques/<str:year_name>/',views.prv_ques),
    path('prv-ques/<str:year_name>/<str:board>/',views.prv_ques2),
    path('prv-ques/<str:year_name>/<str:board>/<str:subject>/',views.prv_year_ques),
    path('course/<str:class_name>/',views.course),
    path('list/<str:class_name>/',views.classsubject),
    path('list/<str:class_name>/<str:sub_name>/',views.subjectquestion),
    path('list/<str:class_name>/<str:sub_name>/<str:chapter_name>/',views.question_list),
    path('list/<str:classes_name>/<str:sub_name>/<str:chapter_name>/<str:type_name>/<int:id>/',views.question),
    path('Practices/<str:classes_name>/<str:sub_name>/<str:chapter_name>/',views.practices),
    path('Written/<str:classes_name>/<str:sub_name>/<str:chapter_name>/',views.written_list),
    path('Written/<str:classes_name>/<str:sub_name>/<str:chapter_name>/<int:id>/',views.written),
    path('Video/<str:classes_name>/<str:sub_name>/<str:chapter_name>/',views.video),
    path('user-reg/', views.user_reg),
    path('result/', views.resultshow),
    path('logout/',views.logout),
    path('contact/',views.contact, name="contact"),
    path('about/',views.about, name="contact"),

    
    #........ Admin Urls..........
    path('dashboard/', views.dashboard),
    path('user-history/', views.history),
    path('user-written-history/', views.written_history),
 
    path('edit-profile/', views.edit_profile),
]
