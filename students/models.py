from django.db import models
from django.contrib.auth.models import User
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save, post_save
from django.core.exceptions import ValidationError



# # Create your models here.
# class Faculty(models.Model):
#     name = models.CharField(max_length=30)

#     def __str__(self) -> str:
#         return self.name
    
#     class Meta:
#         verbose_name = "Faculty"  # Singular name in admin
#         verbose_name_plural = "Faculties"  # Plural name in admin



class Level(models.Model):
    admission_year = models.CharField(max_length=50, blank=True)
    level = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return self.level
    class Meta:
        ordering = ['admission_year']


class Session(models.Model):
    session = models.ForeignKey(Level, on_delete=models.CASCADE)

    # Add any additional fields here
    description = models.TextField()

    

    def save(self, *args, **kwargs):
        # Check if an instance already exists
        if not self.pk and Session.objects.exists():
            raise ValidationError("Only one instance of Session is allowed.")
        return super(Session, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Deletion is not allowed for this model.")
    
   

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Faculty(models.Model):
    name = models.CharField(max_length=300, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Faculty"  # Singular name in admin
        verbose_name_plural = "Faculties"  # Plural name in admin


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, blank=True)

    def __str__(self) -> str:
        return self.name


class StudentProfile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profileimg/', blank=True)
    first_name = models.CharField(max_length=20, blank=True)
    other_names = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    admission_year = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=1000, blank=True)
    nationality = models.CharField(max_length=1000, blank=True)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    inst_email = models.CharField(max_length=50, blank=True)
    email_verified = models.BooleanField(default=False)
    account_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'userprofile'):
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


# Signal to delete the file when a Profile is deleted
@receiver(post_delete, sender=StudentProfile)
def delete_profile_picture_on_delete(sender, instance, **kwargs):
    instance.profile_picture.delete(save=False)

# Signal to delete the old file when the Profile picture is updated
@receiver(pre_save, sender=StudentProfile)
def delete_old_profile_picture_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_profile = StudentProfile.objects.get(pk=instance.pk)
    except StudentProfile.DoesNotExist:
        return False

    new_picture = instance.profile_picture
    old_picture = old_profile.profile_picture

    if old_picture and old_picture != new_picture:
        old_picture.delete(save=False)



