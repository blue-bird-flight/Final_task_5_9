from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_posts = 0
        rating_aut_comments = 0
        rating_comments_posts = 0
        for i in Post.objects.filter(Post_author_id=self.id):  # получаем посты автора
            for j in Comments.objects.filter(Post=i):  # получаем коментарии ко всем статьям автора
                rating_comments_posts += j.Rating_Post
            rating_posts += i.Rating_Post
        for i in Comments.objects.filter(User=self.user):  # получаем коментарии оставленные автором
            rating_aut_comments += i.Rating_Post
        self.rating = rating_posts*3 + rating_aut_comments + rating_comments_posts
        self.save()
        return rating_posts*3 + rating_aut_comments + rating_comments_posts


class Category(models.Model):
    category = models.CharField(max_length=20, unique=True)


class Post(models.Model):
    Post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    Post_News_choice = models.BooleanField(default=False) # False - новость
    Create_time = models.DateTimeField(auto_now_add=True)
    Category = models.ManyToManyField(Category, through='PostCategory')
    Title = models.CharField(max_length=255)
    Text_post = models.TextField()
    Rating_Post = models.IntegerField(default=0)

    def like(self):
        if self.Rating_Post >= 0:
            self.Rating_Post += 1
            self.save()

    def dislike(self):
        if self.Rating_Post >= 1:
            self.Rating_Post -= 1
            self.save()

    def preview(self):
        preview = str(self.Text_post)
        if len(preview) <= 124:
            return preview
        else: return preview[0:124] + '...'


class PostCategory(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comments(models.Model):
    # Методы like() и dislike()
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Text_comment = models.TextField()
    Create_time = models.DateTimeField(auto_now_add=True)
    Rating_Post = models.IntegerField(default=0)

     # повторное написание одинаковых методов модели. как исправить?
    def like(self):
        if self.Rating_Post >= 0:
            self.Rating_Post +=1
            self.save()


    def dislike(self):
        if self.Rating_Post >=1:
            self.Rating_Post -= 1
            self.save()

