from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q,F
from django.http import HttpResponse
from .import models
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q,F
from django.db.models import Sum
from .import models
import datetime
from django.core import serializers
import json
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import random, string, os
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.decorators import login_required
import hashlib, socket
import random


# Create your views here.
def index(request):       
        classsubjects       = models.classsubject.objects.filter(status=True).order_by("classes","subject")
        
      
        context={
            'classsubjects' : classsubjects,
            
          
        }
        return render(request, "blogapp/index.html",context)


def classsubject(request, class_name):
    class_name        = class_name.replace('-', ' ')
    subjects          = models.classsubject.objects.filter(classes_id__name=class_name,status=True).order_by("id")    
    
    
    context={
        'subjects'    : subjects,
       
    }
    return render(request, "blogapp/subject.html",context)


def course(request, class_name):
    class_name        = class_name.replace('-', ' ')
    subjects          = models.classsubject.objects.filter(classes_id__name=class_name,status=True).order_by("id")    
    
    
    context={
        'subjects'    : subjects,
       
    }
    return render(request, "blogapp/course.html",context)





def subjectquestion(request, class_name, sub_name):
        classes_name        = class_name.replace('-', ' ')
        sub_name            = sub_name.replace('-', ' ')
        subjects            = models.subjectchapter.objects.raw("SELECT cs.id, c.name as class_name, s.name,s.image from blogapp_subjectchapter sc INNER JOIN blogapp_classsubject cs on sc.classsubject_id = cs.id  INNER JOIN blogapp_classes c on cs.classes_id = c.id INNER JOIN blogapp_subject s on cs.subject_id = s.id where sc.status = true and c.name = %s GROUP by s.id ORDER by s.id",[classes_name])
        # subjects_questions  = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name,status=True).order_by("subjectchapter")
        subjects_chapter    = models.subjectchapter.objects.filter(classsubject_id__classes_id__name=classes_name, classsubject_id__subject_id__name=sub_name,status=True).order_by("chapter")
        

        context={
            'subjects'    : subjects,
            'subjects_chapter'    : subjects_chapter,
    }
        return render(request, "blogapp/chapter.html",context)


def practices(request,classes_name, sub_name, chapter_name):
    classes_name        = classes_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    chapter_name        = chapter_name.replace('-', ' ')
    ebook           = models.subjectchapter.objects.filter(classsubject_id__classes_id__name=classes_name, classsubject_id__subject_id__name=sub_name, chapter_id__name=chapter_name ,status=True).first()
    context={
        'ebook'    : ebook,
    }
    return render(request, "blogapp/ebook.html",context)

def video(request,classes_name, sub_name, chapter_name):
    classes_name        = classes_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    chapter_name        = chapter_name.replace('-', ' ')
    video           = models.subjectchapter.objects.filter(classsubject_id__classes_id__name=classes_name, classsubject_id__subject_id__name=sub_name, chapter_id__name=chapter_name ,status=True).first()
    context={
        'video'    : video,
    }
    return render(request, "blogapp/video.html",context)

def written(request):

    return render(request, "blogapp/written.html")














def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        massage = request.POST.get('massage')
        models.contact.objects.create(email = email , name = name, massage = massage)
        messages.success(request, "Thankyou for send massage we will give you feedack in your mail")   

    return render(request,'blogapp/contact.html')

def about(request):  

    return render(request,'blogapp/about.html')
