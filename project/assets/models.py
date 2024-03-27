from django.db import models
from django.contrib.auth.models import User

#Create model for Asset
class Asset(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	name = models.CharField(max_length=100, default='something')
	amount = models.IntegerField(default=0)
