"""eval URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from tacos.api import UserProfileResource, UserResource, RecipeResource, StepResource, AllergyResource, \
    IngredientResource, RecipeFavouriteResource, StepIngredientResource
from tacos.views import RecipeList, IndexView, RecipeDetail, IngredientList, AllergiesList, Recipe2Detail, RecipeNotView
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(UserProfileResource())
v1_api.register(UserResource())
v1_api.register(RecipeResource())
v1_api.register(StepResource())
v1_api.register(AllergyResource())
v1_api.register(IngredientResource())
v1_api.register(RecipeFavouriteResource())
v1_api.register(StepIngredientResource())

urlpatterns = [
    # Auth
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^admin', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^recipes/$', RecipeList.as_view(), name='recipes'),
    url(r'^ingredients/$', IngredientList.as_view(), name='ingredients'),
    url(r'^allergies/$', AllergiesList.as_view(), name='allergies'),
    url(r'^recipe/(?P<pk>[-\w]+)/$', RecipeDetail.as_view(), name='recipe-detail'),
    url(r'^recipe2/(?P<pk>[-\w]+)/$', Recipe2Detail.as_view(), name='recipe-detail2'),
    url(r'^recipe-not/$', RecipeNotView.as_view(), name='recipe-not'),

    # API section
    url(r'^api/', include(v1_api.urls)),

    # Catch all non existent pages
    url(r'^.*$', IndexView.as_view(), name='index'),

]
