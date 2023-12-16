from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def softdelete(self):
        self.is_deleted = True
        self.is_active = False
        self.updated = pendulum.now()
        self.save()

    class Meta:
        abstract = True

USER_TYPE =  (
    (1, 'Freelancer'),
    (2, 'Employer')
)

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="profile")
    phone_number = models.CharField(max_length=200,blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    user_type = models.IntegerField(choices=USER_TYPE, default=1, null=True, blank=True)
    portfolio = models.JSONField(default=list, null=True, blank=True)
    category = models.OneToOneField("base.Category", on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey("base.Location", on_delete=models.CASCADE, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    
    
    def __str__(self):
        
        return f"{self.user.first_name} - {self.user.last_name}"
    
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
    

class Category(BaseModel):
    name = models.CharField(max_length=300,blank=True, null=True)
    code = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        
        return self.name
    

class Skill(BaseModel):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=300, blank=True)
    
    def __str__(self):
        
        return self.name
    
class Location(BaseModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        
        return self.name
    
    
    