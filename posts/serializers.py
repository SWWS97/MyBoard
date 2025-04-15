from rest_framework.serializers import ModelSerializer

from posts.models import Post, Comment
from users.serializers import ProfileSerializer

# 게시글 조회를 할 때, 게시글에 작성한 댓글을 보여주고 싶으면
# 게시글 조회 시리얼라이저 코드안에 댓글 조회 시리얼라이저를 넣어 참조한다.
# 하지만 파이썬 코드는 위에서 아래로 읽는다.
# 그렇기 때문에 댓글 시리얼라이저를 위에 정의를 해야 위에서 부터 코드를 읽어가며 찾고
# 참조한 댓글 시리얼라이저가 있다는걸 인지하고 장고가 이해를 한다.

# 게시글 댓글 조회 시리얼라이저
class CommentSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("pk", "profile", "post", "text")

# 게시글 댓글 작성 시리얼라이저
class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "text")

# 게시글 조회 시리얼라이저
class PostSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True) # nested serializer(이중 중첩된 시리얼라이저)
    # 댓글 시리얼라이저를 포함하여 댓글 추가, many=True를 통해 다수의 댓글 포함
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("pk", "profile", "title", "body", "image", "published_date", "likes", 'comments')

# 게시글 작성 시리얼라이저
class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "category", "body", "image")