from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

class Prediction(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    SMOKING_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    REGION_CHOICES = [
        ('northeast', 'Northeast'),
        ('northwest', 'Northwest'),
        ('southeast', 'Southeast'),
        ('southwest', 'Southwest'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    bmi = models.FloatField()
    children = models.IntegerField()
    smoker = models.CharField(max_length=3, choices=SMOKING_CHOICES)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    predicted_cost = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Prediction for {self.user.username}'
