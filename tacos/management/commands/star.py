from django.core.management.base import BaseCommand
from tacos.models import UserProfile, Recipe
from django.db.models import Count
from django.db import connection


class Command(BaseCommand):
    args = 'Arguments are not needed'
    help = 'Mark people with 10 recipes via star, unmark otherwise'

    def my_custom_sql(self):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "UPDATE tacos_userprofile SET star = TRUE WHERE user_id IN " +
                "(SELECT user_id FROM tacos_recipe GROUP BY user_id HAVING COUNT(*) >= 10)")
            cursor.execute(
                "UPDATE tacos_userprofile SET star = FALSE WHERE user_id IN " +
                "(SELECT user_id FROM tacos_recipe GROUP BY user_id HAVING COUNT(*) < 10)")
            return True
        except Exception:
            return False

    def handle(self, *args, **kwargs):
        if self.my_custom_sql():
            self.stdout.write("Success")
        else:
            self.stdout.write("Error")
