import csv
from datetime import datetime
from django.core.management import BaseCommand
from visualize.models import Dengue

class Command(BaseCommand):
    help = 'Import dengue data into PostgreSQL'

    def handle(self, *args, **options):
        file_path = 'dataset/doh-epi-dengue-data-2016-2021 (1).csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Skip rows that start with '#'
                if row['loc'].startswith('#'):
                    continue

                # Convert empty values to None
                for field in ['loc', 'cases', 'deaths', 'date', 'Region']:
                    row[field] = row[field] if row[field] != '' else None

                Dengue.objects.create(
                    loc=row['loc'],
                    cases=int(row['cases']) if row['cases'] else None,
                    deaths=int(row['deaths']) if row['deaths'] else None,
                    date=datetime.strptime(row['date'], '%Y-%m-%d').date() if row['date'] else None,
                    region=row['Region']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))