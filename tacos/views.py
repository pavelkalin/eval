from django.shortcuts import render
from django.views.generic import View, DetailView
from django.core.cache import cache
from .models import Recipe, Ingredient, UserProfile


# Create your views here.

class IndexView(View):
    def get(self, request):
        recipes = Recipe.list_shared(Recipe, request.user.id)
        cache.set("foo", "value", timeout=25)
        context = {
            "recipes": recipes
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


class IngredientDetail(DetailView):
    model = Ingredient
    template_name = "ingredient.html"
