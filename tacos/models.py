from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from tacos.core.models import TimeStampedModel


class UserProfile(TimeStampedModel):
    """
        Additional data about User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    star = models.BooleanField(default=False, verbose_name="Starred?")

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

    def get_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Recipe(TimeStampedModel):
    """
        Recipes data model
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    share = models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile)

    def __str__(self):
        return "Directions for {} are {}".format(self.name, self.list_directions())

    def list_directions(self):
        return ", ".join([step.directions for step in Step.objects.all().filter(recipe__id=self.id)])

    def get_name(self):
        return self.name

    def get_user(self):
        return self.user.get_name()

    def list_shared(self, user_profile_id):
        shared_recipes = [recipe for recipe in Recipe.objects.all().filter(Q(share=True) | Q(user=user_profile_id))]
        return shared_recipes


class Step(TimeStampedModel):
    """
        Steps data model
    """
    step_number = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, related_name="%(class)s_recipe_id", on_delete=models.CASCADE)
    directions = models.TextField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.directions


class Ingredient(TimeStampedModel):
    """
        Ingredients for recipes
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name


class StepIngredient(TimeStampedModel):
    """
        Amount of ingredients for each step in recipe
    """
    recipe = models.ForeignKey(Recipe, related_name="%(class)s_recipe_id", on_delete=models.CASCADE)
    step_number = models.ForeignKey(Step, related_name="%(class)s_step_number", on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, related_name="%(class)s_ingredient_id", on_delete=models.CASCADE)
    quantity = models.CharField(max_length=255)

    def __str__(self):
        return ", ".join(
            [ingredient.name for ingredient in Ingredient.objects.all().filter(stepingredient_ingredient_id=self.id)])

    def get_ingredient(self):
        return self.ingredient_id.get_name()

    def get_user(self):
        return self.recipe.get_user()

    def get_recipe(self):
        return self.recipe.get_name()


class RecipeFavourite(TimeStampedModel):
    """
        Model for storing recipes favourites
    """
    recipe = models.ForeignKey(Recipe, related_name="%(class)s_recipe_id", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name="%(class)s_user_id", on_delete=models.CASCADE)

    # TODO: change later
    def list_favourites(self):
        return ", ".join(
            [recipe.name1 for recipe in Recipe.objects.all().filter(recipefavourite_recipe_id=self.recipe)])

    def get_user(self):
        return self.user.get_name()

    def get_recipe(self):
        return self.recipe.get_name()

    def __str__(self):
        return self.recipe.get_name()


class Allergy(TimeStampedModel):
    """
        Model for storing Allergies with severity of condition
    """
    user = models.ForeignKey(UserProfile, related_name="%(class)s_userprofile_id")
    name = models.CharField(max_length=100)
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HI = "HI"
    severities = ((LOW, "LOW"), (MEDIUM, "MEDIUM"), (HI, "HI"))
    severity = models.CharField(max_length=6, choices=severities, default=severities[1])

    def __str__(self):
        return "{} with {} severity".format(self.name, self.severity)

    def get_user(self):
        return self.user.get_name()

    def get_allergies(self, user_profile_id):
        return [allergy for allergy in Allergy.objects.all().filter(user=user_profile_id)]
