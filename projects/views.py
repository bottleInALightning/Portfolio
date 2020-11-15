from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import re
from Portfolio.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import CommentField,BlogPost,UserProfile,Project
from django.utils import timezone
import string
import smtplib

#from email.MIMEMultipart import MIMEMultipart 
#from email.MIMEText import MIMEText
import secrets

# Create your views here.
def generate_token():
    token_length=6
    digits = string.digits
    token = ''.join(secrets.choice(digits) for i in range(token_length))
    print("super-secret token is ",token)
    return token

def index(request):
    return render(request,"projects/index.html")

def projects(request):
    if request.method=="POST": 
        if request.POST.get("project_title") and request.POST.get("github_link") and request.POST.get("image_link")\
            and request.POST.get("image_width") and request.POST.get("image_height") and request.POST.get("text_field") and request.POST.get("create_project"):
            if request.POST.get("image_width").isdigit() and request.POST.get("image_height").isdigit():
                proj=Project(author=request.user.username,pub_date=timezone.now(),img_link=request.POST.get("image_link"),
                github_link=request.POST.get("github_link"),img_height=request.POST.get("image_height"),img_width=request.POST.get("image_width"),
                text_content=request.POST.get("text_field"),author_id=request.user.id,title=request.POST.get("project_title")
                )
                proj.save()
                return HttpResponseRedirect("")
        if request.POST.get("delete_project"):
            Project.objects.filter(primary_key=request.POST.get("project_id")).delete()
            return HttpResponseRedirect("")
    #will render list of project objects?
    pros=Project.objects.all()

    
    return render(request,"projects/projects.html",{"pros":pros})
    

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
    try:
        email_verified=UserProfile.objects.filter(user_id=request.user.id)[0].email_verified
    except:
        email_verified=False
    comments=CommentField.objects.all()
    return render(request,"projects/comments.html",{"comments":reversed(comments),"email_verified":email_verified})

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
        if request.POST.get("email_input"):
            email_regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.search(email_regex,request.POST["email_input"]) and not User.objects.filter(email=request.POST["email_input"]).exists():
                email_correct=1
                email=request.POST["email_input"]
            else:
                email_correct=0#not valid, email invalid text appears
        else:
            email_correct=2#no input, no "email invalid" text
        if request.POST.get("password_input"):
            if len(request.POST["password_input"])>7:
                password_correct=1
                password=request.POST["password_input"]
            else:
                password_correct=0
        else:
            password_correct=2
        if request.POST.get("username_input"):
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
        
        try:
            if request.user.is_authenticated:
                print("User if authenticated")
                user_profile = UserProfile.objects.filter(user_id=request.user.id)[0]
                print("Found user_profile")
                if request.POST.get("email_auth_code"):

                    print("email auth code was receivable")
                    if user_profile.email_send and not user_profile.email_verified:
                        print("email has been sent AND the user is yet not verified")
                        print("Stored token: ",user_profile.secret_email_auth_token," Received toke:",request.POST.get("email_auth_code"))
                        
                        if request.POST["email_auth_code"] == str(user_profile.secret_email_auth_token):
                            print("updating and saving status")
                            user_profile.email_verified=True
                            user_profile.save(update_fields=["email_verified"])
                            return HttpResponseRedirect("/site/")
        except Exception as a:
            print("EXCEPTION: ",a)
        
    if password_correct == 1 and email_correct == 1 and username_ok==1:
        user=User.objects.create_user(username=username,password=password,date_joined=timezone.now(),email=email)
        account_created=True
        up=UserProfile.objects.create(user_id=user.id,email_verified=False)
        up.save()
        user.save()#maybe this has to go before the other save/creation
        user=authenticate(password=password,username=username)
        print("Auth worked")
        print(user)
        if user != None:
            login(request,user)
        return HttpResponseRedirect("")

    
    user = request.user
    user_profiles = UserProfile.objects.filter(user_id=user.id)
    try:
        user_profile=UserProfile.objects.filter(user_id=user.id)[0]
    except:
        pass

    if request.method=="POST":
        if request.POST.get("resend_code") == "Resend":
            print("Email send now False\n","+"*20)
            user_profile.email_send=False
            user_profile.save(update_fields=["email_send"])
            print("After saving. Email send:",user_profile.email_send)
            
            
    try:
        email_verified=user_profiles[0].email_verified
    except: #could also be that new users don't have corresponding userprofile
        email_verified=False

    try:
        print("User auth: ",request.user.is_authenticated)
        print("Email Send: ",user_profiles[0].email_send)
        print("Email verified: ",user_profiles[0].email_verified)
    except Exception as e:
        print("Except-e:",e)

    if user.is_authenticated and user_profiles[0].email_send==False and not user_profiles[0].email_verified:
        #send email
        print("Sending Email soon ...")
        user_profile=UserProfile.objects.filter(user_id=user.id)[0]
        print("may access user id: (user id) >> ",user.id)
        tken=generate_token()
        print("gen-token returned:",tken)
        user_profile.secret_email_auth_token=tken
        user_profile.save(update_fields=["secret_email_auth_token"])
        
        

        subject="Light Stack Email Authentication"
        
        
        html_message = render_to_string('projects/email_auth_mail_template.html', {'token': user_profile.secret_email_auth_token})
        plain_message = strip_tags(html_message)

        recepient=request.user.email
        send_mail(subject,plain_message, EMAIL_HOST_USER, [recepient],html_message=html_message, fail_silently = False)

        
        
        user_profile.email_send=True
        user_profile.save(update_fields=["email_send"])
    #except Exception as e:
        #print("Tried to access this site with old account")
       # print("Excpetion:",e)

    contexts={"email_correct":str(email_correct),"password_correct":str(password_correct),"username_correct":str(username_ok),
    "account_created":account_created,"email_verified":email_verified}#request.user.UserProfile.email_verified

    return render(request,"projects/register.html",contexts)