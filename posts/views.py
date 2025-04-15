from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Comment
from posts.permissions import CustomReadOnly
from posts.serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer
from users.models import Profile
# view마다 필터 설정할 때 사용(settings.py에 이미 등록해서 상관 없음)
from django_filters.rest_framework import DjangoFilterBackend

# 게시글 전체 목록, 단일 조회, 생성, 수정, 삭제 다 포함 (DRF ModelViewSet 덕분)
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all() # 쿼리셋으로 전체 Post 객체를 가져옴
    permission_classes = [CustomReadOnly] # 권한은 CustomReadOnly로: 조회는 누구나, 수정/삭제는 작성자만
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'likes']

    # 요청 종류에 따라 다른 serializer 사용
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve': # 'list' 또는 'retrieve' 일 경우
            return PostSerializer # 게시글 목록 조회/단일 조회니까 읽기용 PostSerializer
        return PostCreateSerializer # 나머지 (create, update 등) → 쓰기 전용 PostCreateSerializer
    # 이 메서드는 serializer.save() 하기 전에 추가적인 필드 값을 강제로 넣어줄 때 사용
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user) # 현재 로그인한 유저의 프로필 객체 가져오기
        serializer.save(author=self.request.user, profile=profile)
        # serializer.save(...): 이 데이터를 기반으로 Post 객체를 저장하는데,
        # author, profile 값을 명시적으로 채워줌
        # 즉, Post를 새로 만들 때 요청 본문에는 이 값들이 없어도 → 강제로 채워줌!

# 좋아요 기능 FBV(함수형 뷰)
@api_view(['GET']) # 데코레이터로 GET 요청을 받게 설정
@permission_classes([IsAuthenticated]) # 좋아요 누르는 권한은 회원가입하고 로그인한 유저, 즉 인증된 유저 모두 가능
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk) # pk에 해당하는 게시물(Post) 객체를 가져오고 없으면 404 에러
    # 현재 로그인한 유저가 이 글을 좋아요 눌렀는지 체크
    # post.likes.all() 내에 request.user가 있으면 request.user를 지우고
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    # 없으면 request.user 추가(좋아요를 이미 눌렀을 때 다시 누르면 지워지고 아닐때 누르면 좋아요가 생김)
    else:
        post.likes.add(request.user)
    # 성공적으로 처리되면 JSON 응답 {"status": "ok"}을 반환함.
    return Response({'status': 'ok'})

# 게시글 댓글 뷰
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all() # 쿼리셋으로 전체 Comment 객체를 가져옴
    permission_classes = [CustomReadOnly] # 권한은 CustomReadOnly로: 조회는 누구나, 수정/삭제는 작성자만

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return CommentSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user) # 현재 로그인한 유저의 프로필 객체 가져오기
        serializer.save(author=self.request.user, profile=profile)
        # serializer.save(...): 이 데이터를 기반으로 Comment 객체를 저장하는데,
        # author, profile 값을 명시적으로 채워줌
        # 즉, Comment를 새로 만들 때 요청 본문에는 이 값들이 없어도 → 강제로 채워줌!
