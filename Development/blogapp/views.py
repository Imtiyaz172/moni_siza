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
        models.visitor.objects.create() 
        question_counter          = models.question.objects.filter(status=True).count()       
        written_counter          = models.written.objects.filter(status=True).count()       
        view_counter          = models.visitor.objects.filter(status=True)      
        speech          = models.index_speech.objects.filter(status=True)      
        registerd_counter          = models.user_reg.objects.filter(status=True).count()       
        happy          = models.contact.objects.filter(view_in_home=True).order_by("-id")         
             
        classsubjects       = models.classsubject.objects.filter(status=True).order_by("classes","subject")
        if request.method=="POST":
            email     = request.POST['email']
            password  = request.POST['password']

            new_md5_obj = hashlib.md5(password.encode())
            enc_pass    = new_md5_obj.hexdigest()
            user        = models.user_reg.objects.filter(email = email, password = enc_pass)
            if user:
                request.session['email'] = user[0].email
                request.session['id'] = user[0].id
                return redirect("/dashboard/")
        context={
            'classsubjects' : classsubjects,
            'question' : question,
            'speech' : speech,
            'question_counter' : question_counter,
            'written_counter' : written_counter,
            'view_counter' : view_counter,
            'registerd_counter' : registerd_counter,
            'happy' : happy,
          
        }
        return render(request, "blogapp/index.html",context)


def classsubject(request, class_name):
    class_name        = class_name.replace('-', ' ')
    subjects          = models.classsubject.objects.filter(classes_id__name=class_name,status=True).order_by("id")    
    
    
    context={
        'subjects'    : subjects,
       
    }
    return render(request, "blogapp/subject.html",context)





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


def question_list(request, class_name, sub_name, chapter_name):
    classes_name        = class_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    chapter_name        = chapter_name.replace('-', ' ')
    questions_contant_video   = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,status=True).first()
    questions_list      = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,ques_level = "Easy",status=True).order_by("subjectchapter")
    questions_list1      = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,ques_level = "Medium",status=True).order_by("subjectchapter")
    questions_list2      = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,ques_level = "Hard",status=True).order_by("subjectchapter")
    questions_contant   = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,status=True).first() 

    try :
        questions_contant_u = models.user_answer.objects.filter(question_id__subjectchapter_id__chapter_id__name=chapter_name,user_reg_id = request.session['id']).count()
        
        questions_contant1 = models.user_answer.objects.filter(question_id__subjectchapter_id__chapter_id__name=chapter_name, is_correct_ans='True' ,user_reg_id = request.session['id']).count()
        if questions_contant1 == 0:
            questions_contant1 = 1
        if questions_contant_u == 0:
            questions_contant_u = 1
        percentage = questions_contant1 / questions_contant_u * 100
        print(questions_contant1)
        percentage = int(percentage)
        
        if questions_contant_u>25 and questions_contant_u<50 and percentage < 80:
            questions_contant_e   = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,status=True).first()
            print('xxx')
            context={
                
                'questions_contant_e'    : questions_contant_e,
                'questions_list'    : questions_list,
                'questions_contant'    : questions_contant,
            }
            return render(request, "blogapp/question_list.html",context)
        
        if questions_contant_u>50 and percentage < 80:
            questions_contant_e   = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,status=True).first()
            questions_contant_video   = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,status=True).first()
            
            context={
                'questions_contant_e'    : questions_contant_e,
                'questions_contant_video'    : questions_contant_video,
                'questions_list'    : questions_list,
                'questions_contant'    : questions_contant,
                }
            return render(request, "blogapp/question_list.html",context)
    except:
        pass
    context={
        'questions_contant_video'    : questions_contant_video,
        'questions_list'    : questions_list,
        'questions_list1'    : questions_list1,
        'questions_list2'    : questions_list2,
        'questions_contant'    : questions_contant,


        }  
    return render(request, "blogapp/questionlist.html",context)  



    return render(request, "blogapp/questionlist.html",context)

def question(request, classes_name, sub_name, chapter_name,type_name, id):
    classes_name        = classes_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    chapter_name        = chapter_name.replace('-', ' ')
    type_name           = type_name.replace('-', ' ')
    questions           = models.question.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,ques_level=type_name,id=id ,status=True).first()
    if request.method=="POST":
        direct_input_op   = request.POST.get('direct_input_op')
        taketime        = request.POST.get('taketime')
        if 'direct_input_op' in request.POST:
            cheak_ans     = models.question.objects.filter(id=id ,direct_input_op=direct_input_op)
           
            if request.session.get('id'):
                user_ans = models.user_answer.objects.create(
                    user_reg_id = int(request.session['id']), question_id = questions.id,text_choose = direct_input_op, taketime=taketime,
                )
                
                
                if cheak_ans:
                
                    models.user_answer.objects.filter(id = user_ans.id).update(is_correct_ans = True, )
                    messages.success(request, "আপনার উত্তরটি সঠিক হয়েছে")
                    valid_profiles_id_list      = models.question.objects.values_list('id', flat=True).filter(subjectchapter_id__classsubject_id__classes_id__name = classes_name,subjectchapter_id__classsubject_id__subject_id__name=sub_name,subjectchapter_id__chapter_id__name=chapter_name ,ques_level=type_name,status=True).exclude(id = id)

                    valid_profiles_list = random.sample(list(valid_profiles_id_list), len(valid_profiles_id_list))    
                    return redirect("/list"+"/"+classes_name.replace(' ', '-')+"/"+sub_name.replace(' ', '-')+"/"+chapter_name.replace(' ', '-')+"/"+type_name.replace(' ', '-')+"/"+str(valid_profiles_list[0]))
                elif not cheak_ans:
                    messages.warning(request, "আপনার উত্তরটি ভুল হয়েছে")
                
            else:
                if cheak_ans:
                    valid_profiles_id_list      = models.question.objects.values_list('id', flat=True).filter(subjectchapter_id__classsubject_id__classes_id__name = classes_name,subjectchapter_id__classsubject_id__subject_id__name=sub_name,subjectchapter_id__chapter_id__name=chapter_name ,ques_level=type_name,status=True).exclude(id = id)
                    valid_profiles_list = random.sample(list(valid_profiles_id_list), len(valid_profiles_id_list))    
                    messages.success(request, "আপনার উত্তরটি সঠিক হয়েছে.")
                    return redirect("/list"+"/"+classes_name.replace(' ', '-')+"/"+sub_name.replace(' ', '-')+"/"+chapter_name.replace(' ', '-')+"/"+type_name.replace(' ', '-')+"/"+str(valid_profiles_list[0]))
                elif not cheak_ans:
                    messages.warning(request, "আপনার উত্তরটি ভুল হয়েছে")
            # if request.session.get('id'):
            #     get_star  = models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id )    
    
        else:
            ans_op_1        = True if request.POST.get('ans_op_1') else False
            ans_op_2        = True if request.POST.get('ans_op_2') else False
            ans_op_3        = True if request.POST.get('ans_op_3') else False
            ans_op_4        = True if request.POST.get('ans_op_4') else False
            taketime        = request.POST.get('taketime')
            
            

            cheak_ans       = models.question.objects.filter(id=id ,ans_op_1 = ans_op_1,ans_op_2 = ans_op_2,ans_op_3 = ans_op_3,ans_op_4 = ans_op_4)
            if request.session.get('id'):
                user_ans = models.user_answer.objects.create(
                    user_reg_id = int(request.session['id']), question_id =questions.id,ans_choose_op_1 = ans_op_1, ans_choose_op_2 = ans_op_2, ans_choose_op_3 = ans_op_3, ans_choose_op_4 = ans_op_4, taketime=taketime,
                )
                valid_profiles_id_list      = models.question.objects.values_list('id', flat=True).filter(subjectchapter_id__classsubject_id__classes_id__name = classes_name,subjectchapter_id__classsubject_id__subject_id__name=sub_name,subjectchapter_id__chapter_id__name=chapter_name ,ques_level=type_name,status=True).exclude(id = id)

                valid_profiles_list = random.sample(list(valid_profiles_id_list), len(valid_profiles_id_list))    
                # cheak_hit = models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id)
                # if cheak_hit:
                #     models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id).update(hit_count = F('hit_count')+1)
                # else:
                #     hit_count = models.user_hit_count.objects.create(
                #     user_reg_id = int(request.session['id']), question_id = questions.id ,hit_count = 1
                #     )

                # cheak_star_5  = models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id, hit_count = 1, star = 0)
                # cheak_star_4  = models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id, hit_count = 2, star = 0)
                # cheak_star_3  = models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id, hit_count = 3, star = 0)
                # cheak_star_2  = models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id, hit_count = 4, star = 0)
                # cheak_star_1  = models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id,  star = 0)
                if cheak_ans:
                #     if cheak_star_5:
                #         models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id).update(star = F('star')+5)
                #     elif cheak_star_4:
                #         models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id).update(star = F('star')+4)
                #     elif cheak_star_3:
                #         models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id).update(star = F('star')+3)
                #     elif cheak_star_2 :
                #         models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id).update(star = F('star')+2)
                #     elif cheak_star_1 :
                #         models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id).update(star = F('star')+1)
                    models.user_answer.objects.filter(id = user_ans.id).update(is_correct_ans = True )
                    messages.success(request, "আপনার উত্তরটি সঠিক হয়েছে.")
                    return redirect("/list"+"/"+classes_name.replace(' ', '-')+"/"+sub_name.replace(' ', '-')+"/"+chapter_name.replace(' ', '-')+"/"+type_name.replace(' ', '-')+"/"+str(valid_profiles_list[0]))
                   

                elif not cheak_ans:
                    messages.warning(request, "আপনার উত্তরটি ভুল হয়েছে")
                # get_star  = models.user_hit_count.objects.filter(user_reg_id = int(request.session['id']), question_id = questions.id )       
            else:   
                if cheak_ans:
                    valid_profiles_id_list      = models.question.objects.values_list('id', flat=True).filter(subjectchapter_id__classsubject_id__classes_id__name = classes_name,subjectchapter_id__classsubject_id__subject_id__name=sub_name,subjectchapter_id__chapter_id__name=chapter_name ,ques_level=type_name,status=True).exclude(id = id)
                    valid_profiles_list = random.sample(list(valid_profiles_id_list), len(valid_profiles_id_list))    
                    messages.success(request, "আপনার উত্তরটি সঠিক হয়েছে.")
                    return redirect("/list"+"/"+classes_name.replace(' ', '-')+"/"+sub_name.replace(' ', '-')+"/"+chapter_name.replace(' ', '-')+"/"+type_name.replace(' ', '-')+"/"+str(valid_profiles_list[0]))
                elif not cheak_ans:
                    messages.warning(request, "আপনার উত্তরটি ভুল হয়েছে")
            
                
    
    else:
        messages.warning(request, "")
    
    
    
    context={
        'questions'    : questions,
        # 'get_star'    : get_star,
        

}
    return render(request, "blogapp/question.html",context)


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

def written_list(request,classes_name, sub_name, chapter_name):
    classes_name        = classes_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    chapter_name        = chapter_name.replace('-', ' ')
    written_list           = models.written.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name ,status=True).all()
    context={
        'written_list'    : written_list,
    }
    return render(request, "blogapp/writtenlist.html",context)



def written(request,classes_name, sub_name, chapter_name,id):
    classes_name        = classes_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    chapter_name        = chapter_name.replace('-', ' ')
    written           = models.written.objects.filter(subjectchapter_id__classsubject_id__classes_id__name=classes_name, subjectchapter_id__classsubject_id__subject_id__name=sub_name, subjectchapter_id__chapter_id__name=chapter_name,id=id ,status=True).first()
    if request.method=="POST":
        ans = ""
        if bool(request.FILES.get('ans', False)) == True:
            file = request.FILES['ans']
            ans = "written/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"written/"):
                os.mkdir(settings.MEDIA_ROOT+"written/")
            default_storage.save(settings.MEDIA_ROOT+"written/"+file.name, ContentFile(file.read()))
        models.user_written_answer.objects.create(
            user_reg_id = int(request.session['id']), question_id = written.id,ans = ans,
            )    
    context={
        'written'    : written,
    }
    return render(request, "blogapp/written.html",context)




def user_reg(request):
    if request.method=="POST":
        f_name            = request.POST['f_name']
        l_name            = request.POST['l_name']
        email           = request.POST['email']
        date_of_birth           = request.POST['date_of_birth']
        mobile           = request.POST['mobile']
        password        = request.POST['password']
        new_md5_obj     = hashlib.md5(password.encode())
        new_enc_pass    = new_md5_obj.hexdigest()
        cheak_email     = models.user_reg.objects.filter(email = email)

        if not cheak_email:
            models.user_reg.objects.create(f_name=f_name,l_name=l_name,mobile=mobile,date_of_birth=date_of_birth,  email = email, password = new_enc_pass)
            messages.success(request, "আপনার রেজিস্ট্রেশন সফল হয়েছে । আপনার একাউন্টে লগ-ইন করুন")
            return redirect('/')
        else:
            messages.warning(request, "এই ইমেইল দিয়ে একটি একাউন্ট আছে । একাউন্টে লগ-ইন করুন")
            return redirect('/')
    else:
        messages.warning(request, "")
    return render(request, "blogapp/signup.html")



def login(request):
    if request.method=="POST":
        email     = request.POST['email']
        password  = request.POST['password']

        new_md5_obj = hashlib.md5(password.encode())
        enc_pass    = new_md5_obj.hexdigest()
        user        = models.user_reg.objects.filter(email = email, password = enc_pass)
        if user:
            request.session['email'] = user[0].email
            request.session['id'] = user[0].id
            return redirect("/")
    
    return render(request, "blogapp/admin/login.html")

def logout(request):
    request.session['email'] = False
    request.session['id'] = False
    return redirect("/")


def course(request, class_name):
    class_name        = class_name.replace('-', ' ')
    subjects          = models.classsubject.objects.filter(classes_id__name=class_name,status=True).order_by("id")    
    context={
        'subjects':subjects,
    }
    return render(request, "blogapp/course.html",context)




def prv_ques(request, year_name):
    year_name        = year_name.replace('-', ' ')
    question          = models.board_on_year.objects.filter(year_id__year=year_name,status=True).order_by("id")    
    context={
        'question':question,
    }
    return render(request, "blogapp/pre_sub_selection.html",context)



def prv_ques2(request, year_name,board):
    year_name        = year_name.replace('-', ' ')
    board            = board.replace('-', ' ')
    question2          = models.board_on_year.objects.filter(status=True).order_by("id")    
    question          = models.prev_year_ques.objects.filter(year_and_board_id__year_id__year=year_name,year_and_board_id__board_id__name=board,status=True).order_by("id")    
    context={
        'question2':question2,
        'question':question,
    }
    return render(request, "blogapp/pre_sub_selection2.html",context)




def prv_year_ques(request, year_name,board,subject):
    year_name        = year_name.replace('-', ' ')
    board            = board.replace('-', ' ')
    subject            = subject.replace('-', ' ')  
    prv_question          = models.prev_year_ques.objects.filter(year_and_board_id__year_id__year=year_name,year_and_board_id__board_id__name=board,subject_id__name=subject,status=True).first()
    
    context={
        
        'prv_question':prv_question,
    }
    return render(request, "blogapp/ebook2.html",context)


















# .................................... For Admin..................................................

def dashboard (request):
    if not request.session['id']:
        return redirect('/')
    user_profile      = models.user_reg.objects.filter(status = True, id = request.session['id']).first()
    mcq_count      = models.user_answer.objects.filter(user_reg_id = request.session['id']).count()
    written_count      = models.user_written_answer.objects.filter(user_reg_id = request.session['id']).count()
    context={
        'user_profile'    : user_profile,
        'mcq_count'    : mcq_count,
        'written_count'    : written_count,
}
    return render(request, "blogapp/user_panel/index.html",context)

def history (request):
    if not request.session['id']:
        return redirect('/login/')
    user_history      = models.user_answer.objects.filter(status = True, user_reg_id = request.session['id']).order_by("-id")
    
    
        
    context={
        'user_history'    : user_history,
}
    return render(request, "blogapp/user_panel/user_history.html",context)

def written_history (request):
    if not request.session['id']:
        return redirect('/login/')
    user_history      = models.user_written_answer.objects.filter( user_reg_id = request.session['id']).order_by("-id")
    
    
        
    context={
        'user_history'    : user_history,
}
    return render(request, "blogapp/user_panel/history.html",context)


def subjectresult(request):
    if not request.session['id']:
        return redirect('/login/')
    
    classes    = models.classsubject.objects.filter(status=True).all()
    
    context={
        'classes'    : classes,
}
    return render(request, "blogapp/admin/classlist.html",context)

def classlistimprove(request):
    if not request.session['id']:
        return redirect('/login/')
    
    classes    = models.classsubject.objects.filter(status=True).all()
    
    context={
        'classes'    : classes,
}
    return render(request, "blogapp/admin/classlist_improvement.html",context)


def subjectlist(request, class_name):
    class_name        = class_name.replace('-', ' ')
    if not request.session['id']:
        return redirect('/login/')
    
    
    subjectsre   = models.classsubject.objects.filter(classes_id__name=class_name,status=True).order_by("id")
        

    context={
        'subjectsre'    : subjectsre,
    }
    return render(request, "blogapp/admin/subject_res.html",context)
        
def subjectlistimprovement(request, class_name):
    class_name        = class_name.replace('-', ' ')
    if not request.session['id']:
        return redirect('/login/')
    
    
    subjectsre   = models.classsubject.objects.filter(classes_id__name=class_name,status=True).order_by("id")
        

    context={
        'subjectsre'    : subjectsre,
    }
    return render(request, "blogapp/admin/subject_imp.html",context)


def chapter_list_improvement(request, class_name,sub_name):
    class_name        = class_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    if not request.session['id']:
        return redirect('/login/')
    
    chapter_list   = models.subjectchapter.objects.filter(classsubject_id__classes_id__name=class_name, classsubject_id__subject_id__name=sub_name,status=True).order_by("id")

    
    context={
        'chapter_list'    : chapter_list,
        
    }
    return render(request, "blogapp/admin/chapter_imp.html",context)


def improvement(request, class_name,sub_name,chapter_name):
    class_name        = class_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    chapter_name        = chapter_name.replace('-', ' ')
    if not request.session['id']:
        return redirect('/login/')
    
    all_ques_c     =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name ,question_id__subjectchapter_id__chapter_id__name=chapter_name ,user_reg_id = request.session['id']).count()
    secound     =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name ,question_id__subjectchapter_id__chapter_id__name=chapter_name ,is_correct_ans='True',user_reg_id = request.session['id'])[:50].count()
    all_ans     =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name ,question_id__subjectchapter_id__chapter_id__name=chapter_name ,is_correct_ans='True',user_reg_id = request.session['id']).count()
    all_ques50     =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name ,question_id__subjectchapter_id__chapter_id__name=chapter_name ,user_reg_id = request.session['id'])[:50]
    all_ques25     =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name ,question_id__subjectchapter_id__chapter_id__name=chapter_name ,user_reg_id = request.session['id'])[:25]
    all_ques     =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name ,question_id__subjectchapter_id__chapter_id__name=chapter_name ,user_reg_id = request.session['id'])
    # all_ques = int(all_ques)
    correct_count = 0
    correct_count25 = 0
    correct_count50 = 0
    for i in all_ques:
        if i.is_correct_ans: correct_count += 1
        print(i.is_correct_ans,i.id)
    for i in all_ques25:
        if i.is_correct_ans: correct_count25 += 1
        print(i.is_correct_ans,i.id)
    for i in all_ques50:
        if i.is_correct_ans: correct_count50 += 1
        print(i.is_correct_ans,i.id)

    # all_ques = all_ques.filter(is_correct_ans=True)

    # if all_ques < 25:
    #     first_persent = first / all_ques * 100
     
    # if all_ques > 25:
    #     first_persent = first / 25 * 100
    #     print(first_persent)

    # if all_ques < 50:
    #     secound_persent = secound / all_ques * 100
    #     print(secound_persent)
        
    # if all_ques > 50:
    #     all_ans_persent = all_ans / all_ques * 100
   
    context={
    
    # 'all_ans_persent'    : all_ans_persent,
    'correct_count'    : correct_count,
    'correct_count25'    : correct_count25,
    'correct_count50'    : correct_count50,
    'all_ques_c'    : all_ques_c,
    # 'first_persent'    : first_persent,
    # 'secound_persent'    : secound_persent,
    
}
    
    
    return render(request, "blogapp/admin/improvment.html",context)



def subjectperform(request, class_name,sub_name):
    class_name        = class_name.replace('-', ' ')
    sub_name            = sub_name.replace('-', ' ')
    
    if not request.session['id']:
        return redirect('/login/')
    

    answerd    =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name ,user_reg_id = request.session['id']).count()
    right      =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name, is_correct_ans='True' ,user_reg_id = request.session['id']).count()
    wrong      =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name, is_correct_ans='False' ,user_reg_id = request.session['id']).count()
    spend      =  models.user_answer.objects.filter(question_id__subjectchapter_id__classsubject_id__subject_id__name=sub_name ,question_id__subjectchapter_id__classsubject_id__classes_id__name=class_name ,user_reg_id = request.session['id']).aggregate(Sum('taketime'))['taketime__sum'],
    spend = float('.'.join(str(ele) for ele in spend))
    context={
        'answerd'    : answerd,
        'right'    : right,
        'wrong'    : wrong,
        'spend'    : spend,
    }
    return render(request, "blogapp/admin/result.html",context)

   





def edit_profile (request):
    if not request.session['id']:
        return redirect('/login/')
    edit_profile      = models.user_reg.objects.filter(status = True, id = request.session['id']).first()
    context={
        'edit_profile' : edit_profile,
    }
    if request.method=="POST":
        name                = request.POST['name']
        address             = request.POST['address']
        school              = request.POST['school']
        classes             = request.POST['classes']
        roll                = request.POST['roll']
        user_type           = str(request.POST['user_type'])

        if edit_profile and edit_profile.user_image:  
            user_image = edit_profile.user_image
        else:
            user_image = ""   
        if bool(request.FILES.get('user_image', False)) == True:
            if os.path.exists('/static/blogapp/media/'+str(user_image)):
                os.remove('/static/blogapp/media/'+str(user_image))
            file = request.FILES['user_image']
            user_image = "user_image/"+file.name
            if not os.path.exists(settings.MEDIA_ROOT+"user_image/"):
                os.mkdir(settings.MEDIA_ROOT+"user_image/")
            default_storage.save(settings.MEDIA_ROOT+user_image, ContentFile(file.read()))

        models.user_reg.objects.filter(id = request.session['id']).update(name = name, user_image = user_image, address = address,  school = school, classes_id = classes, roll = roll, user_type_str = user_type )
        
        return redirect('/dashboard/')
    return render(request, "blogapp/admin/edit_profile.html",context)





def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        massage = request.POST.get('massage')
        models.contact.objects.create(email = email , name = name, massage = massage)
        messages.success(request, "Thankyou for send massage we will give you feedack in your mail")   

    return render(request,'blogapp/connectus.html')

def about(request):  

    return render(request,'blogapp/about.html')
