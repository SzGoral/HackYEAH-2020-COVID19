# Generated by Django 2.2.1 on 2019-06-01 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retina', '0005_remove_rawdata_pattern_fil2sade'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdata',
            name='movie_number',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
