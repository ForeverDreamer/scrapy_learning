from django.db import models


# 产品
class Product(models.Model):
    title = models.CharField(max_length=120)
    desc = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # objects = ProductManager()

    def __str__(self):
        return self.title
