from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Recipe, Step, StepIngredient, Ingredient, UserProfile, Allergy, RecipeFavourite
from .forms import UserCreationForm


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Recipes description", {"fields": ["name", "description"]}),
        ("Recipes duration in minutes", {"fields": ["duration"]})
    ]

    # list_editable = ("duration",)

    def recipe_directions(self, obj: Recipe):
        return obj.list_directions()

    recipe_directions.short_description = "Directions"

    list_display = ("name", "description", "duration", "recipe_directions",)
    list_display_links = ("name", "description", "duration",)
    list_filter = ("duration",)
    search_fields = ("name",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # list_display = ("first_name", "last_name", "star",)
    readonly_fields = ("star",)


class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ("name", "severity", "get_user")

    def get_user(self, obj: UserProfile):
        return obj.get_user()

    get_user.short_description = "User"


@admin.register(RecipeFavourite)
class RecipeFavouriteAdmin(admin.ModelAdmin):
    list_display = ("get_recipe", "get_user")

    def get_user(self, obj):
        return obj.get_user()

    def get_recipe(self, obj):
        return obj.get_recipe()

    get_user.short_description = "User"
    get_recipe.short_description = "Recipe name"

admin.site.register(Step)
admin.site.register(StepIngredient)
admin.site.register(Ingredient)
