from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView

from .models import Recipe, Ingredient, Allergy, RecipeFavourite, StepIngredient, Step


# Create your views here.

class IndexView(View):
    """Default view for renedering home page and all nonexistent pages"""
    def get(self, request):
        recipes = Recipe.list_shared(Recipe, request.user.id)
        context = {
            "recipes": recipes,
            "title": "Best tacos app ever"
        }

        return render(request, "index.html", context)


class RecipeNotView(View):
    """Default view for nonexisted recipes or nonshared once"""

    def get(self, request):
        context = {
            "title": "Try your luck next time"
        }

        return render(request, "recipenot.html", context)

class RecipeList(View):
    """Default common view to list all recipes"""
    def get(self, request):
        recipes = Recipe().list_shared(request.user.id)
        context = {
            "recipes": recipes,
            "test": cache.get("foo")
        }

        return render(request, "recipes.html", context)


class Recipe2Detail(DetailView):
    """Basic detail view of recipes"""
    model = Recipe
    template_name = "recipe.html"


class RecipeDetail(LoginRequiredMixin, DetailView):
    """DetailView of each recipe either owned or shared"""
    model = Recipe
    step_ingredients = None
    is_favourite = None
    steps = None
    allergies = None
    template_name = "recipe2.html"
    login_url = '/login/'
    redirect_field_name = 'next'

    def get_cache(self):
        allergy = cache.get(self.request.user.id)
        if allergy:
            return allergy
        else:
            cache.set(self.request.user.id,
                      [allergy.name for allergy in Allergy.objects.all().filter(user_id=self.request.user.id)], 300)
            allergy = cache.get(self.request.user.id)
            return allergy

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            return redirect('recipe-not')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def set_context(self):
        self.step_ingredients = StepIngredient.objects.all().filter(recipe_id=self.kwargs['pk']).prefetch_related()
        self.is_favourite = RecipeFavourite.objects.all().filter(recipe_id=self.kwargs['pk']).filter(
            user_id=self.request.user.id)
        self.steps = Step.objects.all().filter(recipe_id=self.kwargs['pk'])
        self.allergies = self.get_cache()

        return True

    def get_queryset(self):
        self.get_cache()
        self.set_context()
        recipe = Recipe.objects.all().filter(Q(share=True) | Q(user_id=self.request.user.id))
        if recipe:
            return recipe
        else:
            return Recipe.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["step_ingredients"] = self.step_ingredients
        context["favourites"] = self.is_favourite
        context["steps"] = self.steps
        context["allergies"] = self.allergies
        context["title"] = "Detailed view of recipe"

        return context


class IngredientList(ListView):
    model = Ingredient
    template_name = "ingredient.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "List of ingredients"
        return context


class AllergiesList(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        allergies = Allergy().get_allergies(request.user.id)
        context = {
            "allergies": allergies,
            "title": "List of my allergies",
        }

        return render(request, "allergy.html", context)
