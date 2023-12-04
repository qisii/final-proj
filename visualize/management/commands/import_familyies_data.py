import csv
from django.core.management.base import BaseCommand
from visualize.models import FamilyIncomeExpenditure  

class Command(BaseCommand):
    help = 'Import Filipino Family Income and Expenditure data into PostgreSQL'

    def handle(self, *args, **options):
        file_path = 'dataset/filipino_family_expenditure.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:

                FamilyIncomeExpenditure.objects.create(
                    region=row['Region'],
                    income=row['Total Household Income'],
                    food=row['Total Food Expenditure'],
                    rice=row['Total Rice Expenditure'],
                    bread_cereal=row['Bread and Cereals Expenditure'],
                    meat=row['Meat Expenditure'],
                    fish=row['Total Fish and  marine products Expenditure'],
                    fruits=row['Fruit Expenditure'],
                    vegetables=row['Vegetables Expenditure'],
                    hotels=row['Restaurant and hotels Expenditure'],
                    alcohol=row['Alcoholic Beverages Expenditure'],
                    tobacco=row['Tobacco Expenditure'],
                    clothing=row['Clothing, Footwear and Other Wear Expenditure'],
                    housing=row['Housing and water Expenditure'],
                    medical=row['Medical Care Expenditure'],
                    transport=row['Transportation Expenditure'],
                    communication=row['Communication Expenditure'],
                    education=row['Education Expenditure'],
                    miscellaneous=row['Miscellaneous Goods and Services Expenditure'],
                    occasions=row['Special Occasions Expenditure'],
                    farming=row['Crop Farming and Gardening expenses'],
                )
        self.stdout.write(self.style.SUCCESS('Filipino Family Income and Expenditure data imported successfully'))