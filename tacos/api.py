from tastypie.resources import ModelResource
from tastypie import fields
from .models import UserProfile, Recipe, Step, Ingredient, StepIngredient, RecipeFavourite, Allergy
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization


class UserResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = User.objects.all()
        resource_name = 'user_base'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'id', 'date_joined']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class UserProfileResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        always_return_data = True
        queryset = UserProfile.objects.all()
        list_allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        detail_allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        resource_name = 'user'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class RecipeResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = Recipe.objects.all()
        resource_name = 'recipe'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class StepResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = Step.objects.all()
        resource_name = 'step'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class IngredientResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = Ingredient.objects.all()
        resource_name = 'ingredient'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class StepIngredientResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = StepIngredient.objects.all()
        resource_name = 'step_ingredient'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class RecipeFavouriteResource(ModelResource):
    recipe = fields.ForeignKey(RecipeResource, 'recipe', full=True)

    class Meta:
        always_return_data = True
        queryset = RecipeFavourite.objects.all()
        resource_name = 'favourite'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class AllergyResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = Allergy.objects.all()
        resource_name = 'allergy'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
