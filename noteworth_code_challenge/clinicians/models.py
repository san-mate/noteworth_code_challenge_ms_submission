from django.db import models


class Clinician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    clinic_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id} - {self.first_name} {self.last_name}'
