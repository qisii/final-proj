from django.db import models

# Create your models here.

# Dengue Data Model
class Dengue(models.Model):
    loc = models.CharField(max_length=255, null=True, blank=True)
    cases = models.IntegerField(null=True, blank=True)
    deaths = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.loc} - {self.date}"
    # class Meta:
    #     db_table = 'dengue'

# Pizza Hut Data Model
class PizzaHutLocation(models.Model):
    type = models.CharField(max_length=255, null=True, blank=True)
    address_1 = models.CharField(max_length=255, null=True, blank=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    open_hours = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.address_1}, {self.city}, {self.state} {self.postal_code}"

# Family IES Data Model
class FamilyIncomeExpenditure(models.Model):
    region = models.CharField(max_length=255, null=True, blank=True)
    income = models.IntegerField(null=True, blank=True)
    food = models.IntegerField(null=True, blank=True)
    rice = models.IntegerField(null=True, blank=True)
    bread_cereal = models.IntegerField(null=True, blank=True)
    meat = models.IntegerField(null=True, blank=True)
    fish = models.IntegerField(null=True, blank=True)
    fruits = models.IntegerField(null=True, blank=True)
    vegetables = models.IntegerField(null=True, blank=True)
    hotels = models.IntegerField(null=True, blank=True)
    alcohol = models.IntegerField(null=True, blank=True)
    tobacco = models.IntegerField(null=True, blank=True)
    clothing = models.IntegerField(null=True, blank=True)
    housing = models.IntegerField(null=True, blank=True)
    medical = models.IntegerField(null=True, blank=True)
    transport = models.IntegerField(null=True, blank=True)
    communication = models.IntegerField(null=True, blank=True)
    education = models.IntegerField(null=True, blank=True)
    miscellaneous = models.IntegerField(null=True, blank=True)
    occasions = models.IntegerField(null=True, blank=True)
    farming = models.IntegerField(null=True, blank=True)
