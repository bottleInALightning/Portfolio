from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user_id=models.IntegerField(verbose_name="ID of user linked to this userprofile",default=-1)
    description="User class to store data about a user"
    email_verified=models.BooleanField(verbose_name="email authenticated or not",default=0)
    secret_email_auth_token=models.IntegerField(default=-1)    
    email_send=models.BooleanField(verbose_name="email sent",default=False)
    

'''
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)'''
class Project(models.Model):
    primary_key=models.AutoField(verbose_name="pk",primary_key=True)                #primary key
    author=models.CharField(verbose_name="author username", max_length=26)          #author username
    pub_date=models.DateTimeField(verbose_name="data of release")                   #the date of posting
    img_link=models.CharField(verbose_name="link to image included",max_length=150) #a link to a thumbnail image
    github_link=models.CharField(verbose_name="link to github repo",max_length=160) #a link to the projects repo
    img_width=models.IntegerField(verbose_name="image_width")                       #the images width
    img_height=models.IntegerField(verbose_name="image_height")                     #the images height
    text_content=models.CharField(verbose_name="project description",max_length=1500)#the project description
    author_id=models.IntegerField(verbose_name="Id of author")                      #the authors id
    title=models.CharField(verbose_name="Project title",max_length=200)             #The projects name

    def __str__(self):
        return f"pk:{self.primary_key} title:{self.title}"
        
class CommentField(models.Model):
    primary_key=models.AutoField(verbose_name="primary key", primary_key=True)
    pub_date=models.DateTimeField(verbose_name="Date Field")
    text_content=models.TextField(verbose_name="Text Field",max_length=300,null=False)#maybe null= False will make Troubles
    author=models.CharField(verbose_name="Author",max_length=26)
    author_id=models.IntegerField(verbose_name="author_id",default=-1)

    def __str__(self):
        return f"pk:{self.primary_key} text:{self.text_content} pub-date:{self.pub_date}"

class BlogPost(models.Model):

    primary_key=models.AutoField(verbose_name="pk", primary_key=True)
    pub_date=models.DateTimeField(verbose_name="Published Date")
    title=models.TextField(verbose_name="Title")
    img_link=models.TextField(verbose_name="img link")#have to include the "None" option
    img_width=models.IntegerField(verbose_name="image widht",default=300)
    img_height=models.IntegerField(verbose_name="image heigth",default=200)

    text_content=models.TextField(verbose_name="text_content")
    author=models.CharField(verbose_name="Author",max_length=30)
    author_id=models.IntegerField(verbose_name="Author id")
