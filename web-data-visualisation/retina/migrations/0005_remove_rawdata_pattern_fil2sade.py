# Generated by Django 2.2.1 on 2019-05-22 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retina', '0004_rawdata_pattern_fil2sade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawdata',
            name='pattern_fil2sade',
        ),
    ]
