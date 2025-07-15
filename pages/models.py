# pages/models.py

import string
import random
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, title, new_slug=None):
    """
    Genera un slug basado en `title`. Si ya existe en la BD, 
    le añade un sufijo aleatorio y vuelve a comprobar recursivamente.
    """
    slug = new_slug or slugify(title)
    Klass = instance.__class__
    if Klass.objects.filter(slug=slug).exists():
        # añade un sufijo y prueba de nuevo
        new_slug = f"{slug}-{random_string_generator()}"
        return unique_slug_generator(instance, title, new_slug=new_slug)
    return slug

class Page(models.Model):
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True, blank=True)
    content     = models.TextField()
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Si no tiene slug, lo generamos
        if not self.slug:
            self.slug = unique_slug_generator(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
