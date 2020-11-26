from django.db import models

 
 
class ApplicationFeatures(models.Model):
    signup = models.BooleanField()
    limit_user_signup = models.BooleanField(default=False)