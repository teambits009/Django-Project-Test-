# import necessary modules
import os
import django
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangosearchproject.settings')  # Change 'myproject.settings' to your project's settings
django.setup()

# import your model
from searchapp.models import Item

# create Faker instance
fake = Faker()

# generate and save instances of Item
for _ in range(10):  # Change 10 to the desired number of instances
    name = fake.word()
    description = fake.text()

    item = Item.objects.create(name=name, description=description)
    item.save()

print("Data population complete.")
