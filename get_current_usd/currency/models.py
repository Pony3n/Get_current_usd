from django.db import models

class Currency(models.Model):
    current_rate = models.DecimalField(max_digits=10, decimal_places=2)
    time_code = models.DateTimeField(auto_now_add=True)

