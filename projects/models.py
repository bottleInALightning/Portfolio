from django.db import models

# Create your models here.
class UserField(models.Field):
    description="User class to store data about a user"


    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        super().__init__(*args, **kwargs)

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
    author=models.CharField(verbose_name="Author",max_length=30)#maybemakecommentonthisbutton,thathaslike@new_stuffblablaincommentsection
    author_id=models.IntegerField(verbose_name="Author id")
