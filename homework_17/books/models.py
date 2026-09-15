from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
    )

    slug = models.SlugField(
        unique=True,
        verbose_name=_("Slug"),
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=_("Title"),
    )

    author = models.CharField(
        max_length=200,
        verbose_name=_("Author"),
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )

    stock = models.IntegerField(
        verbose_name=_("Stock"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Category"),
    )

    def __str__(self):
        return self.title