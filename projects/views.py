from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import re
from .models import CommentField,BlogPost
from django.utils import timezone
# Create your views here.


def index(request):
    return render(request,"projects/index.html")

def projects(request):
    return render(request,"projects/projects.html")

def personal(request):
    return render(request,"projects/personal.html")
def blog(request):
    
    
    if request.method=="POST":
        print(request.POST)
        try:
            if request.POST["contents"] and request.POST["title"]:
                img_w=300
                img_h=200
                if request.POST["image_width"]:
                    img_w=int(request.POST["image_width"])
                if request.POST["image_height"]:
                    img_h=int(request.POST["image_height"])
                post=BlogPost(pub_date=timezone.now(),text_content=request.POST["contents"],author=request.user.username,author_id=request.user.id,title=request.POST["title"],img_link=request.POST["img_link"],img_height=img_h,img_width=img_w)
                post.save()
                return HttpResponseRedirect("/site/blog")
            
        except  Exception as e:
            print(e)
        
        try:
            if request.POST["delete_button"]:
                print("DElete blog with Id:",request.POST["delete_blog_id"])
                BlogPost.objects.filter(primary_key=request.POST["delete_blog_id"]).delete()
                return HttpResponseRedirect("")
        except Exception as e:
            print(e)
    blogs=reversed(BlogPost.objects.all())
    return render(request,"projects/blog.html",{"blogs":blogs})



def comment(request):
    if request.method=="POST":
        print("Post request:",request.POST)
        try:
            if request.POST["comment_text"].strip():
                if request.POST["comment_text"] != "" and len(request.POST["comment_text"])<300:
                    new_comment = CommentField(pub_date=timezone.now(),text_content=request.POST["comment_text"],author=request.user.username,author_id = request.user.id)
                    new_comment.save()
                    return HttpResponseRedirect("/site/comments/")
        except Exception as e:
            print("Error:",e)
        try:
            if request.POST["delete_comment"]:
                print("Delete button clicked!")
                if request.POST["comment_id"]:#{%if request.user.is_staff or comment.author_id == request.user.primary_key %}
                    
                    CommentField.objects.filter(primary_key=request.POST["comment_id"]).delete()
                    #return HttpResponseRedirect("/site/comments/")
        except Exception as e:
            print("Error:",e)
    
    comments=CommentField.objects.all()
    return render(request,"projects/comments.html",{"comments":reversed(comments)})

def login_page(request):
    wrong_input=False
    if request.method=="POST":
        print("user active:",request.user.is_active)
        
        password=request.POST["password_input"]
        username=request.POST["email_input"]
        user=authenticate(password=password,username=username)
        if user !=None:
            login(request,user)
        wrong_input=False
        if not request.user.is_active:
            wrong_input=True

    return render(request,"projects/login.html",{"wrong_input":wrong_input})
def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/site/")
def register(request):
    email=""
    password=""
    account_created=False
    email_correct=2
    password_correct=2
    username=""
    username_ok=2
    if request.method=="POST":
        if request.POST["email_input"]:
            email_regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.search(email_regex,request.POST["email_input"]) and not User.objects.filter(email=request.POST["email_input"]).exists():
                email_correct=1
                email=request.POST["email_input"]
            else:
                email_correct=0#not valid, email invalid text appears
        else:
            email_correct=2#not input, no "email invalid" text
        if request.POST["password_input"]:
            if len(request.POST["password_input"])>7:
                password_correct=1
                password=request.POST["password_input"]
            else:
                password_correct=0
        else:
            password_correct=2
        if request.POST["username_input"]:
            if 3<len(request.POST["username_input"])<25:
                if not User.objects.filter(username=request.POST["username_input"]):
                    username_ok=1
                    username=request.POST["username_input"]
                else:
                    username_ok=4
            else:
                username_ok=0
                print("invalid input")
        else:
            username_ok=2
    if password_correct ==1 and email_correct ==1 and username_ok==1:
        user=User.objects.create_user(username=username,password=password,date_joined=timezone.now(),email=email)
        account_created=True
        user.save()
        user=authenticate(password=password,username=username)
        print("Auth worked")
        print(user)
        if user != None:
            login(request,user)
        return HttpResponseRedirect("/site/")
    contexts={"email_correct":str(email_correct),"password_correct":str(password_correct),"username_correct":str(username_ok),"account_created":account_created}
    return render(request,"projects/register.html",contexts)