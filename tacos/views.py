from django.shortcuts import render
from django.views.generic import View, DetailView
from .models import Recipe, Ingredient


# Create your views here.

class IndexView(View):
    def get(self, request):
        recipes = Recipe.objects.all()

        context = {
            "recipes": recipes
        }

        return render(request, "base.html", context)


class RecipeList(View):
    def get(self, request):
        recipes = Recipe.objects.all()

        context = {
            "recipes": recipes
        }

        return render(request, "recipes.html", context)


class IngredientDetail(DetailView):
    model = Ingredient
    template_name = "ingredient.html"
