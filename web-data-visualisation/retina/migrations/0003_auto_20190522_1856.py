# Generated by Django 2.2.1 on 2019-05-22 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retina', '0002_authgroup_authgrouppermissions_authpermission_authuser_authusergroups_authuseruserpermissions_blogpo'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataxxx', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'data_folder',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experimentname', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'experiment',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('px_my', models.CharField(blank=True, max_length=150, null=True)),
                ('pattern_file', models.CharField(blank=True, max_length=150, null=True)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='retina.DataFolder')),
            ],
            options={
                'db_table': 'raw_data',
                'managed': True,
            },
        ),
        migrations.DeleteModel(
            name='AuthGroup',
        ),
        migrations.DeleteModel(
            name='AuthGroupPermissions',
        ),
        migrations.DeleteModel(
            name='AuthPermission',
        ),
        migrations.DeleteModel(
            name='AuthUser',
        ),
        migrations.DeleteModel(
            name='AuthUserGroups',
        ),
        migrations.DeleteModel(
            name='AuthUserUserPermissions',
        ),
        migrations.DeleteModel(
            name='DjangoAdminLog',
        ),
        migrations.DeleteModel(
            name='DjangoContentType',
        ),
        migrations.DeleteModel(
            name='DjangoMigrations',
        ),
        migrations.DeleteModel(
            name='DjangoSession',
        ),
        migrations.AddField(
            model_name='datafolder',
            name='exp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='retina.Experiment'),
        ),
    ]