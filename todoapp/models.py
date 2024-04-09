from django.db import models
from django.urls import reverse
from django.utils import timezone


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)
class TodoList(models.Model):
    title = models.CharField(max_length=225)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=one_week_hence)
    category = models.ForeignKey('Category', default='general', on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse('item-update', args=[str(self.category.id), str(self.id)])

    def __str__(self):
        return f'{self.title}: end {self.end_date}'

    class Meta:
        ordering = ['end_date']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')

    def get_absolute_url(self):
        return reverse('list', args=[self.id])

    def __str__(self):
        return self.name
