# ./manage.py shell < make_fake_users.py
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

# Delete all users
User.objects.all().delete()

# Generate 30 random emails and iterate them.
for email in [fake.unique.email() for i in range(10)]:
    # Create user in database
    my_user = User.objects.get_or_create(
        email=email,
        username=fake.user_name(),
        is_active=True,
    )
    # Set password: 'password'
    my_user_db = User.objects.get(email=email)
    my_user_db.set_password("password")
    my_user_db.save()