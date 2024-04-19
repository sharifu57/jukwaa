from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User


# Create your models here.
class Featured(BaseModel):
    title = models.CharField(null=True, blank=True, max_length=200)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="featured", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Featured"
        verbose_name_plural = "Features"
    def __str__(self):

        return self.title

class Story(BaseModel):
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    crated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"
    def __str__(self):

        return self.title