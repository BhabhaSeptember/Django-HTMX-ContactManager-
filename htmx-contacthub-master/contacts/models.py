from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
# Inherit Django’s built-in user with username, email, password, etc.
# `pass` means “no extra fields… for now”
    pass

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
     # Separate field for images (will show previews)
    image = CloudinaryField(
        'image',
        resource_type='image',  # This will show previews
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        blank=True,
        null=True
    )
    
    # Edited field to use Cloudinary
    document = CloudinaryField(
        'document',
        resource_type='raw',  # Use 'raw' for documents like pdf, docx, txt, images
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt', 'jpg', 'png'])],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='contacts' # lets us do user.contacts.all()
        )  

# Creates constraint in database between user and email
# One user cannot have two contacts with the same email
    class Meta:
        unique_together = ('user', 'email')
    

    def __str__(self):
        return f"{self.name} <{self.email}>"