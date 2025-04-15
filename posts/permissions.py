from rest_framework import permissions


# 글 조회 : 누구나 가능, 생성 : 로그인한 유저만 가능, 편집 : 글 작성자만 가능
class CustomReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET": # GET 요청이면 모든 유저 조회 허용
            return True
        return request.user.is_authenticated # 그외 요청이면 로그인 여부 검사 했으면 True, 안 했으면 False
    # 이 메서드는 특정 객체 단위(한 게시글 등)에 대한 접근 허용 여부를 판단
    def has_object_permission(self, request, view, obj):
        # permissions.SAFE_METHODS는 ["GET", "HEAD", "OPTIONS"] 이건 "조회만 하는 안전한 메서드"
        if request.method in permissions.SAFE_METHODS: # 위의 메서드면 True
            return True
        # 수정/삭제(PUT/PATCH/DELETE) 요청이면 객체의 author가 현재 요청한 user랑 같은지 비교
        return obj.author == request.user
