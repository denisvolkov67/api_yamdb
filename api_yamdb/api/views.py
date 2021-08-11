from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from reviews.models import Categories, Genres, Title, User
from rest_framework import filters, mixins, viewsets, status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.tokens import default_token_generator  

from .permissions import IsAdmin, IsMeUser
from .serializers import (CategoriesSerializer,
                          GenresSerializer, SignupSerializer,
                          TitleSerializer, TokenSerializer, UserMeSerializer, UserSerializer)
from .utils import Util


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    pass


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )


class GenresViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin) 
    lookup_field = 'username'

    # @action(methods=['get', 'patch'], detail=True, url_path='me')
    # def me(self, request):
    #     serializer = UserMeSerializer
    #     if request.method == 'PATCH':
    #         return Response(f'Получены данные: {request.PATCH}')
    #     user = User.objects.filter(username=request.user.username)
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data) 


class UserMeViewSet(RetrieveUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated, IsMeUser)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        return super().perform_update(serializer)


class SignupViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
        
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        username = request.data['username']
        email = request.data['email']
        user = get_object_or_404(User, username = username)
        confirmation_code = default_token_generator.make_token(user)
        data = {
            'email_body': confirmation_code,
            'to_email': email,
            'email_subject': 'confirmation_code'
        }
        Util.send_email(data)
        content  = {
            'username': username,
            'email': email
        }
        return Response(content, status=status.HTTP_200_OK)    


class TokenViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def create(self, request):
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )

    