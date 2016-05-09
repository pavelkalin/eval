from tastypie.resources import ModelResource
from tastypie import fields
from .models import UserProfile
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user_base'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'id', 'date_joined']
        authentication = ApiKeyAuthentication()


class UserProfileResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user'
        authentication = ApiKeyAuthentication()
