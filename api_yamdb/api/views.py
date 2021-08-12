from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviews.models import Categories, Genres, Title, User, UserRole
from rest_framework import filters, mixins, viewsets, status
from rest_framework_simplejwt.tokens import AccessToken
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
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'

    @action(methods=['get', 'patch', 'post'], permission_classes=(IsAuthenticated,), detail=False, url_path='me')
    def me(self, request):
        if request.method == 'GET':
            user = get_object_or_404(User, username=request.user.username)
            serializer = self.get_serializer(user)
            return Response(serializer.data) 

        if request.method == 'PATCH':
            data = request.data
            if request.user.role == UserRole.USER:
                _mutable = data._mutable
                data._mutable = True
                data.update({'role': 'user'})
                data._mutable = _mutable
            serializer = self.get_serializer(request.user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.update(request.user, data)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)



class UserMeViewSet(RetrieveUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        print(request.user.username)
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data) 


class SignupViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
        
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        username = request.data.get('username')
        email = request.data.get('email')
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
        print(request.data)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )

    