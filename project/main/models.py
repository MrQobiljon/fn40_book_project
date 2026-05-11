from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Pk: {self.pk}. Name: {self.name}"


class Book(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_year = models.PositiveSmallIntegerField(default=datetime.now().year)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True,
                             validators=[FileExtensionValidator(['mp4', 'avi'], 'Faqat .mp4 va .avi formatidagi videolarga ruxsat berilagan!')])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="books")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Pk: {self.pk}. Name: {self.name}"


class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Pk: {self.pk}. Name: {self.text}"

