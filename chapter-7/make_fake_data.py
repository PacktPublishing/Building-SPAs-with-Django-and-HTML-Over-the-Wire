# ./manage.py shell < make_fake_data.py
from app.website.models import Post, Comment
from faker import Faker

# Delete all posts and comments
Post.objects.all().delete()

# Create fake object
fake = Faker()


def get_full_name():
    return f"{fake.first_name()} {fake.last_name()}"


# Create 30 posts
for _ in range(30):
    post = Post(
        title=fake.sentence()[:200],
        content=fake.text(),
        author=get_full_name()[:20],
    )
    post.save()

# Create 150 comments
for _ in range(150):
    comment = Comment(
        author=get_full_name()[:20],
        content=fake.text(),
        post=Post.objects.order_by("?").first(),
    )
    comment.save()
