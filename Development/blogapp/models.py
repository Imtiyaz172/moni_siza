from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe 
import os

# Create your models here.


class about_us(models.Model):
    title       = models.CharField(max_length=50)
    logo        = models.ImageField(upload_to="logo/",blank= True)
    phone       = models.CharField(max_length=16,blank=True)
    email       = models.CharField(max_length=36,blank=True)
    address     = models.CharField(max_length=76,blank=True)
    facebook    = models.CharField(max_length=276,blank=True)
    twiter      = models.CharField(max_length=76,blank=True)
    location    = models.TextField(blank=True)
    status      = models.BooleanField(default = True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'about_us'
        verbose_name_plural = 'about_us' 


class index_speech(models.Model):
    title       = models.CharField(max_length=50)
    image        = models.ImageField(upload_to="logo/",blank= True)
    
    speech    = models.TextField(blank=True)
    status      = models.BooleanField(default = True)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'index speech'
        verbose_name_plural = 'index speech' 




class contact(models.Model):
    name          = models.CharField(max_length=100,blank= True)
    email          = models.CharField(max_length=100,blank= True)
    massage          = models.TextField(blank= True)
    time          = models.DateTimeField(auto_now_add = True)
    view_in_home        = models.BooleanField(default = False)

    def __str__(self):
        return self.name     
    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contact' 






class classes(models.Model):
    name          = models.CharField(max_length=100)
    image         = models.FileField(upload_to="class/",blank= True)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.name     
    class Meta:
        verbose_name = 'classes'
        verbose_name_plural = 'classes'  


class subject(models.Model):
    name          = models.CharField(max_length=100)
    image         = models.FileField(upload_to="subject/",blank= True)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.name     
    class Meta:
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'  


class classsubject(models.Model):
    name          = models.CharField(max_length=100,blank= True)
    subject       = models.ForeignKey(subject, on_delete=models.CASCADE)
    classes       = models.ForeignKey(classes, on_delete=models.CASCADE)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.name     
    class Meta:
        verbose_name = 'class and subject'
        verbose_name_plural = 'classes and subjects' 

 

class chapter(models.Model):
    name          = models.CharField(max_length=100,blank= True)
    
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.name     
    class Meta:
        verbose_name = 'chapter'
        verbose_name_plural = 'chapters' 




class subjectchapter(models.Model):
    name          = models.CharField(max_length=200,blank= True)
    chapter       = models.ForeignKey(chapter, on_delete=models.CASCADE)
    classsubject  = models.ForeignKey(classsubject, on_delete=models.CASCADE)
    ebook         = models.FileField(upload_to="ebook/",blank= True)
    Chapter_video_1 = models.TextField(blank=True)
    Chapter_video_2 = models.TextField(blank=True)
    Chapter_video_3 = models.TextField(blank=True)
    Chapter_video_4 = models.TextField(blank=True)
    Chapter_video_5 = models.TextField(blank=True)
    Chapter_video_6 = models.TextField(blank=True)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.name     
    class Meta:
        verbose_name = 'chapter of subject'
        verbose_name_plural = 'chapters of subjects' 



class written(models.Model):
    subjectchapter  = models.ForeignKey(subjectchapter, on_delete=models.CASCADE)
    title           = models.CharField(max_length=200,blank= True)
    body            = RichTextField(blank=True)
    pdf             = models.FileField(upload_to="pdf/",blank= True)
    
    status          = models.BooleanField(default = True)

    def __str__(self):
        return self.title     
    class Meta:
        verbose_name = 'written'
        verbose_name_plural = 'written' 






class question(models.Model):
    subjectchapter  = models.ForeignKey(subjectchapter, on_delete=models.CASCADE)
    ques_type = (
        ('MCQ', 'MCQ'),
        ('Multiple_MCQ', 'Multiple_MCQ'),
        ('text', 'text'),
        
    )
    ques_type       = models.CharField(max_length=20, choices=ques_type)
    ques_level = (
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),    
        ('Easy', 'Easy'),
    )
    ques_level      = models.CharField(max_length=20, choices=ques_level)
    title           = models.CharField(max_length=200,blank= True)
    body            = RichTextField(blank=True)
    image           = models.FileField(upload_to="question/",blank= True)
    direct_input_op = models.CharField(max_length=200,blank= True)
    text_op_1       = models.CharField(max_length=50,blank= True)
    text_op_2       = models.CharField(max_length=50,blank= True)
    text_op_3       = models.CharField(max_length=50,blank= True)
    text_op_4       = models.CharField(max_length=50,blank= True)
    ans_op_1        = models.BooleanField(default = False)
    ans_op_2        = models.BooleanField(default = False)
    ans_op_3        = models.BooleanField(default = False)
    ans_op_4        = models.BooleanField(default = False)
    hint            = RichTextField(blank=True)
    status          = models.BooleanField(default = True)

    def __str__(self):
        return self.title     
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions' 



class user_reg(models.Model):
    f_name               = models.CharField(max_length=100)
    l_name               = models.CharField(max_length=100, blank=True)
    email              = models.EmailField(max_length=80, blank=True)
    mobile             = models.CharField(max_length=18, blank=True)
    password           = models.CharField(max_length=100)
    date_of_birth            = models.CharField(max_length=80,blank=True)
    reg_date           = models.DateField(auto_now_add=True)

    status            = models.BooleanField(default=True)
    def __str__(self):
        return self.f_name     
    class Meta:
        verbose_name = 'User information'
        verbose_name_plural = 'Users informations' 


class user_answer(models.Model):
    user_reg      = models.ForeignKey(user_reg, on_delete=models.CASCADE)
    question      = models.ForeignKey(question, on_delete=models.CASCADE)
    text_choose   = models.CharField(max_length=50,blank= True)
    ans_choose_op_1      = models.BooleanField(default = False)
    ans_choose_op_2      = models.BooleanField(default = False)
    ans_choose_op_3      = models.BooleanField(default = False)
    ans_choose_op_4      = models.BooleanField(default = False)
    is_correct_ans  = models.BooleanField(default = False)
    time          = models.DateTimeField(auto_now_add = True)
    taketime   = models.CharField(max_length=50,blank= True)
    mark          = models.IntegerField(default=0)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return str(self.user_reg)     
    class Meta:
        verbose_name = 'user_answer'
        verbose_name_plural = 'user_answers' 

class user_written_answer(models.Model):
    user_reg      = models.ForeignKey(user_reg, on_delete=models.CASCADE)
    question      = models.ForeignKey(written, on_delete=models.CASCADE)
    ans             = models.FileField(upload_to="ans/",blank= True) 
    mark          = models.FloatField(default = 0,blank= True)
    time          = models.DateTimeField(auto_now_add = True)
    status        = models.BooleanField(default = False)

    def __str__(self):
        return str(self.user_reg)     
    class Meta:
        verbose_name = 'User written answer'
        verbose_name_plural = 'User written answers' 

class user_mark_count(models.Model):
    user_reg      = models.ForeignKey(user_reg, on_delete=models.CASCADE)
    subjectchapter  = models.ForeignKey(subjectchapter, on_delete=models.CASCADE)
    mark          = models.IntegerField(default=0)
    status        = models.BooleanField(default = False)

    def __str__(self):
        return str(self.user_reg)     
    class Meta:
        verbose_name = 'user_mark_count'
        verbose_name_plural = 'user_mark_count' 


class user_hit_count(models.Model):
    user_reg      = models.ForeignKey(user_reg, on_delete=models.CASCADE)
    hit_count      = models.IntegerField(default=0)
    star          = models.IntegerField(default=0)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return str(self.user_reg)     
    class Meta:
        verbose_name = 'user_hit_count'
        verbose_name_plural = 'user_hit_counts' 

class visitor(models.Model):
    count          = models.IntegerField(default=0,blank= True)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.count     
    class Meta:
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitor' 



class classes_on_year(models.Model):
    classes       = models.ForeignKey(classes, on_delete=models.CASCADE,null=True)
    years          = models.CharField(max_length=5,blank= True,null=True)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.years     
    class Meta:
        verbose_name = 'classes_on_year'
        verbose_name_plural = 'classes_on_year' 


class board_on_year(models.Model):
    name          = models.CharField(max_length=100,blank= True,null=True)
    classes_on_year          = models.ForeignKey(classes_on_year, on_delete=models.CASCADE,null=True)
    board         = models.CharField(max_length=55,blank= True,null=True)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.name     
    class Meta:
        verbose_name = 'board_on_year'
        verbose_name_plural = 'board_on_year' 

 



class prev_year_ques(models.Model):
    name          = models.CharField(max_length=100,blank= True)
    year_and_board          = models.ForeignKey(board_on_year, on_delete=models.CASCADE,blank= True,null=True)
    subject         = models.ForeignKey(subject, on_delete=models.CASCADE,blank= True,null=True)
    question      = models.FileField(upload_to="prev_year_ques/",blank= True)
    status        = models.BooleanField(default = True)

    def __str__(self):
        return self.name     
    class Meta:
        verbose_name = 'prev_year_ques'
        verbose_name_plural = 'prev_year_ques' 

 