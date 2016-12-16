from __future__ import unicode_literals
from ..login.models import User
from django.db import models

# Create your models here.
class itemManager(models.Manager):
    #creates a new item with a many t omany relationship with the user who creates it
    def create_item(self, postData, user_id):
        errors = []
        response = {}
        if self.filter(name = postData['item']):
            errors.append('**This item has already been added!**')
        if not len(postData['item']) >= 3:
            errors.append('**Item must contain at least 3 characters**')
        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            response['status'] = True
            user = User.objects.get(id = user_id)
            item = Item.objects.create(name = postData['item'], added_by_name = user.first_name, added_by_id = user_id)
            item.user.add(user)
        return response

    #deletes item from the database
    def delete(self, id):
        Item.objects.get(id=id).delete()
        return ##is this dumb?

    #adds item from wishlist to user's wishlist by estalishing many to many relaitonship
    def add(self, item_id, user_id):
        user = User.objects.get(id = user_id)
        item = Item.objects.get(id= item_id)
        item.user.add(user)
        return

    #remove item from user's wishlist by removing many to many relationship
    def remove(self, item_id, user_id):
        user = User.objects.get(id = user_id)
        item = Item.objects.get(id= item_id)
        item.user.remove(user)
        return

class Item(models.Model):
    name = models.CharField(max_length = 255)
    added_by_name = models.CharField(max_length = 255)
    added_by_id = models.IntegerField()
    user = models.ManyToManyField(User, related_name = "wish_items")
    created_at = models.DateTimeField(auto_now_add = True)
    apdated_at = models.DateTimeField(auto_now = True)
    objects = itemManager()
