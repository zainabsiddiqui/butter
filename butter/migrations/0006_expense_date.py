# Generated by Django 3.0.4 on 2020-04-12 19:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butter', '0005_expense_in_or_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
    ]