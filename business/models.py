from django.db import models
from account.models import User

class BusinessInfo(models.Model):
    user = models.ForeignKey(User, related_name='businessuser', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Creative Poultry Business')
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    description = models.TextField(null=False)
    profile_image = models.ImageField(null=True, upload_to='business-profile-pics')

    def __str__(self) -> str:
        return self.name
    