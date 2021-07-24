# Generated by Django 3.1.13 on 2021-07-23 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursetracker', '0015_auto_20210722_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='corequisites',
        ),
        migrations.RemoveField(
            model_name='course',
            name='dependencies',
        ),
        migrations.AlterField(
            model_name='course',
            name='course_link',
            field=models.CharField(default='err', max_length=200),
        ),
        migrations.AlterField(
            model_name='course',
            name='distribution',
            field=models.CharField(default='err', max_length=70),
        ),
        migrations.AlterField(
            model_name='course',
            name='sub_name',
            field=models.CharField(default='err', max_length=200),
        ),
    ]
