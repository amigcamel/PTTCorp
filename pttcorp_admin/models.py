from django.db import models

import datetime


class UpdateLogModel(models.Model):
    update_message = models.CharField(max_length=500)
    update_datetime = models.DateTimeField(auto_now_add=True, blank=True)
