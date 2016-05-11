from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import deprecate_current_app
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, resolve_url
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, DetailView

from .models import Recipe, Ingredient


# Create your views here.

class IndexView(View):
    def get(self, request):
        recipes = Recipe.list_shared(Recipe, request.user.id)
        cache.set("foo", "value", timeout=25)
        context = {
            "recipes": recipes,
            "title": "Best tacos app ever"
        }

        return render(request, "base.html", context)


class RecipeList(View):
    def get(self, request):
        print(request.user.id)
        recipes = Recipe().list_shared(request.user.id)

        context = {
            "recipes": recipes,
            "test": cache.get("foo")
        }

        return render(request, "recipes.html", context)


class RecipeDetail(DetailView):
    model = Recipe
    template_name = "recipe.html"

class IngredientDetail(DetailView):
    model = Ingredient
    template_name = "ingredient.html"
