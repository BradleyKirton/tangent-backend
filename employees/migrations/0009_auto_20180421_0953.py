# Generated by Django 2.0.4 on 2018-04-21 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_auto_20180421_0952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='positionhistory',
            old_name='review',
            new_name='reviews',
        ),
    ]