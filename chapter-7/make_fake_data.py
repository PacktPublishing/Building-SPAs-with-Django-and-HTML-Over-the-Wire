# ./manage.py shell < make_fake_data.py
from app.website.models import Post, Comment
from faker import Faker

# Delete all posts and comments
Post.objects.all().delete()

# Create fake object
fake = Faker()

# Create 30 posts
for _ in range(30):
    post = Post(
        title=fake.sentence()[:200],
        author=fake.fullname()[:20],
        content=fake.text(),
    )
    post.save()

# Create 150 comments
for _ in range(150):
    comment = Comment(
        author=fake.fullname()[:20],
        content=fake.text(),
        post=Post.objects.order_by("?").first(),
    )
    comment.save()
