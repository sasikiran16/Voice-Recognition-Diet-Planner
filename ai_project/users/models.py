from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class userdetails(models.Model): 
    # id = models.AutoField(primary_key=True, default=1)
    user_name = models.TextField(max_length=10,null=True,unique=True)
    name = models.CharField(max_length=20,null = True) 
    date = models.DateField(auto_now_add=True, null=True)     
    state = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)   
    gender = models.CharField(max_length=20, null=True)
    food_type= models.CharField(max_length=20, null=True)
    food_preference = models.CharField(max_length=30, null=True)
    
class fitnessmen(models.Model): 
    user_name = models.TextField(max_length=10)     
    date = models.DateField(default=date.today) 
    Height = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Weight  = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    activity = models.CharField(max_length=20, null=True)
    goals = models.CharField(max_length=20, null=True)
    goalweight = models.IntegerField(null=True)
    weekly_goal = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    Abdomen = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Neck = models.DecimalField(max_digits=10, decimal_places=2, null=True)
   
class fitnesswomen(models.Model): 
    user_name = models.TextField(max_length=10, null=True)
    date = models.DateField(default=date.today)
    Height = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Weight  = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    activity = models.CharField(max_length=20, null=True)
    goals = models.CharField(max_length=20, null=True)
    goalweight = models.IntegerField(null=True)
    weekly_goal = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    Hip = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Waist = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Neck = models.DecimalField(max_digits=10, decimal_places=2, null=True)
 


class Breakfast(models.Model):
    food_id = models.IntegerField(null=True)
    user_name = models.TextField(max_length=10, null=True)
    date = models.DateField(auto_now_add=True)
    food_names = models.CharField(max_length=20, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    unit = models.CharField(max_length=20, null=True)
    calories = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    proteins = models.IntegerField(null=True)
    fats = models.IntegerField(null=True)



class Lunch(models.Model):
    food_id = models.IntegerField(null=True)
    user_name = models.TextField(max_length=10, null=True)
    date = models.DateField(auto_now_add=True)
    food_names = models.CharField(max_length=20, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    unit = models.CharField(max_length=20, null=True)
    calories = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    proteins = models.IntegerField(null=True)
    fats = models.IntegerField(null=True)


class Snacks(models.Model):
    food_id = models.IntegerField(null=True)
    user_name = models.TextField(max_length=10, null=True)
    date = models.DateField(auto_now_add=True)
    food_names = models.CharField(max_length=20, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    unit = models.CharField(max_length=20, null=True)
    calories = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    proteins = models.IntegerField(null=True)
    fats = models.IntegerField(null=True)


class Dinner(models.Model):
    food_id = models.IntegerField(null=True)
    user_name = models.TextField(max_length=10, null=True)
    date = models.DateField(auto_now_add=True)
    food_names = models.CharField(max_length=20, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    unit = models.CharField(max_length=20, null=True)
    calories = models.IntegerField(null=True)
    carbs = models.IntegerField(null=True)
    proteins = models.IntegerField(null=True)
    fats = models.IntegerField(null=True)


class Water(models.Model):
    user_name = models.TextField(max_length=10, null=True)
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Likes(models.Model):
    user_name = models.TextField(max_length=10, null=True)
    food_names = models.CharField(max_length=20, null=True)

class Dislikes(models.Model):
    user_name = models.TextField(max_length=10, null=True)
    food_names = models.CharField(max_length=20, null=True)


    