from django.db import models

class Users(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    account_number = models.CharField(max_length=18, unique=True)
    name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField()
    dob = models.DateField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name