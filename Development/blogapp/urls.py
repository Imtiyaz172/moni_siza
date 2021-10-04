
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('prv-ques/<str:year_name>/<str:board_name>',views.prv_ques),
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
    path('login/', views.login),
    path('logout/',views.logout),
    path('contact/',views.contact, name="contact"),
    path('about/',views.about, name="contact"),

    
    #........ Admin Urls..........
    path('dashboard/', views.dashboard),
    path('user-history/', views.history),
    path('sub-result/<str:class_name>/',views.subjectlist),
    path('sub-result/<str:class_name>/<str:sub_name>/',views.subjectperform),
    path('class-list-improvement/', views.classlistimprove),
    path('sub-list-improvement/<str:class_name>/',views.subjectlistimprovement),
    path('chapter-list-improvement/<str:class_name>/<str:sub_name>/',views.chapter_list_improvement),
    path('improvement/<str:class_name>/<str:sub_name>/<str:chapter_name>/',views.improvement),
    path('edit-profile/', views.edit_profile),
]
