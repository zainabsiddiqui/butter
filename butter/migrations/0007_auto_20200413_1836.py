# Generated by Django 3.0.5 on 2020-04-13 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('butter', '0006_expense_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ('-date',)},
        ),
    ]
