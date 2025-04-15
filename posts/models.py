from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from users.models import Profile


# 게시글 모델
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  # 게시글 작성자
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)  # 작성자 프로필
    title = models.CharField(max_length=128)    # 게시글 제목
    category = models.CharField(max_length=128) # 게시글 카테고리
    body = models.TextField()   # 게시글 본문
    image = models.ImageField(upload_to='post/', default='default.png') # 이미지
    likes = models.ManyToManyField(User, related_name="like_posts", blank=True) # 게시글 좋아요 누른 사람들
    published_date = models.DateTimeField(default=timezone.now) # 게시글 작성 시간

# 댓글 모델
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글 작성자
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # 댓글 작성자 프로필
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) # 댓글 작성에 필요한 게시글
    text = models.TextField() # 댓글 본문