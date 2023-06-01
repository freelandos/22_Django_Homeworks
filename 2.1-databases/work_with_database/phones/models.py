from django.db import models
from django.template.defaultfilters import slugify


class Phone(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    price = models.PositiveIntegerField(verbose_name='Цена')
    image = models.ImageField(null=True, blank=True, verbose_name='Фото')
    release_date = models.DateField(verbose_name='Дата выпуска')
    lte_exists = models.BooleanField(default=False, verbose_name='Поддержка LTE')
    slug = models.SlugField(max_length=150, unique=True, null=False, verbose_name='URL')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
