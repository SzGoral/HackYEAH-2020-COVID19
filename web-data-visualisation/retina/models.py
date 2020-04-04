from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
import os


class DataFolder(models.Model):
    dataxxx = models.CharField(max_length=150, blank=True, null=True)
    exp = models.ForeignKey('Experiment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_folder'

    def __str__(self):
        return self.dataxxx


class Experiment(models.Model):
    experimentname = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'experiment'

    def __str__(self):
        return self.experimentname

    def get_name(self):
        if self.experimentname is not None:
            return os.path.basename(self.experimentname)


class RawData(models.Model):
    pattern_number = models.IntegerField(blank=True, null=True)
    px_my = models.CharField(max_length=150, blank=True, null=True)
    pattern_file = models.CharField(max_length=150, blank=True, null=True)
    data = models.ForeignKey(DataFolder, models.DO_NOTHING)
    movie_number = models.IntegerField(null=True)

    def __str__(self):
        return self.px_my

    class Meta:
        managed = False
        db_table = 'raw_data'
