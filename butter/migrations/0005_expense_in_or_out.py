# Generated by Django 3.0.4 on 2020-04-12 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butter', '0004_auto_20200411_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='in_or_out',
            field=models.CharField(default='Outflow', max_length=20),
            preserve_default=False,
        ),
    ]