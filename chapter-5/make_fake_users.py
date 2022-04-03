# ./manage.py shell < make_fake_users.py
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

# Delete all users
User.objects.all().delete()

# Generate 30 random emails and iterate them.
for email in [fake.unique.email() for i in range(5)]:
    # Create user in database
    user = User.objects.create_user(fake.user_name(), email, 'password')
    user.last_name = fake.last_name()
    user.is_active = True
    user.save()