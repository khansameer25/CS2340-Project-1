from django.db import models
from movies.models import Movie
from django.contrib.auth.models import User

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def update_total(self):
        self.total = sum(item.price * item.quantity for item in self.item_set.all())
        self.save()

    def __str__(self):
        return str(self.id) + ' - ' + self.user.username

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Set the price based on the associated movie
        self.price = self.movie.price
        super().save(*args, **kwargs)
        self.order.update_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total()

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name