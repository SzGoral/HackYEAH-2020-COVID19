# Generated by Django 2.2.1 on 2019-06-27 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retina', '0008_auto_20190622_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawdata',
            name='pattern_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]