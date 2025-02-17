from django.db import models
from movies.models import Movie
from django.contrib.auth.models import User
# Create your models here.

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id} - {self.user.username}"
    
    def add_movie(self, movie, quantity=1):
        """ Adds a movie to the order or updates the quantity if it already exists. """
        item, created = Item.objects.get_or_create(order=self, movie=movie, defaults={'price': movie.price, 'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save()
        self.update_total()

    def remove_movie(self, movie):
        """ Removes a movie from the order. """
        try:
            item = Item.objects.get(order=self, movie=movie)
            item.delete()
            self.update_total()
        except Item.DoesNotExist:
            pass

    def update_total(self):
        """ Updates the order total based on the current items. """
        self.total = sum(item.price * item.quantity for item in self.item_set.all())
        self.save()

    
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order,
        on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name