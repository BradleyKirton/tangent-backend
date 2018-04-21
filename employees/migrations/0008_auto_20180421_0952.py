# Generated by Django 2.0.4 on 2018-04-21 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_auto_20180421_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='positionhistory',
            name='review',
        ),
        migrations.AddField(
            model_name='positionhistory',
            name='review',
            field=models.ManyToManyField(related_name='positions', to='employees.Review'),
        ),
    ]