import factory

from books.models import Book, Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f"Book {n}")
    author = factory.Sequence(lambda n: f"Author {n}")
    price = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=2,
        positive=True,
    )
    description = factory.Faker("text", max_nb_chars=200)
    stock = factory.Faker("random_int", min=1, max=100)
    category = factory.SubFactory(CategoryFactory)