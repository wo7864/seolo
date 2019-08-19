from django.db import models

class WiseSaying(models.Model):
    name = models.TextField(null=True)
    param1 = models.TextField(null=True)
    param2 = models.TextField(null=True)
    param3 = models.TextField(null=True)
    param4 = models.TextField(null=True)
    param5 = models.TextField(null=True)

    def __str__(self):
        return self.name
