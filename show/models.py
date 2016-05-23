from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Test(models.Model):
    code = models.CharField(max_length=3)
    is_real = models.BooleanField(default=False)


class Airport(models.Model):
    code = models.CharField(max_length=3)  # in now, may be change in the future
    name = models.CharField(max_length=20)  # can change ---
    area = models.CharField(max_length=10)
    area_id = models.IntegerField(default=0)


class PathManager(models.Manager):
    def get_connecting_route(self, des, dep):
        try:
            return self.get(destination_port=des, departure_port=dep, transfer_flag=1)
        except self.model.DoesNotExist:
            return None


class Path(models.Model):
    departure_port = models.CharField(max_length=3, default='XXX')
    destination_port = models.CharField(max_length=3, default='XXX')
    search_flag = models.BooleanField(default=False)
    transfer_flag = models.BooleanField(default=True)
    direct_flag = models.BooleanField(default=False)
    lcc_flag = models.BooleanField(default=False)
    old_stop = models.CharField(max_length=15, default='', null=True)
    new_top = models.CharField(max_length=15, default='')
    is_exist = models.BooleanField(default=True)

    objects = PathManager()


# drop this too @@
class Flightpath(models.Model):
    departure_port = models.CharField(max_length=3, default='XXX')
    destination_port = models.CharField(max_length=3, default='XXX')
    search_flag = models.BooleanField(default=False)
    transfer_flag = models.BooleanField(default=True)
    direct_flag = models.BooleanField(default=False)
    lcc_flag = models.BooleanField(default=False)
    old_stop = models.CharField(max_length=15, default='', null=True)
    new_top = models.CharField(max_length=15, default='')
    is_exist = models.BooleanField(default=True)


# dont use this anymore
class Flypath(models.Model):
    # departure_port = models.CharField(max_length=3)
    # destination_port = models.CharField(max_length=3)
    departure_port = models.CharField(max_length=3, default='XXX')
    destination_port = models.CharField(max_length=3, default='XXX')
    search_flag = models.BooleanField(default=False)
    transfer_flag = models.BooleanField(default=True)
    direct_flag = models.BooleanField(default=False)
    lcc_flag = models.BooleanField(default=False)
    old_stop = models.CharField(max_length=15, default='')
    new_top = models.CharField(max_length=15, default='')
    is_exist = models.BooleanField(default=True)
