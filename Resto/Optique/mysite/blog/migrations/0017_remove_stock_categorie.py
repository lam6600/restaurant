# Generated by Django 4.2.1 on 2023-07-24 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_stock_categorie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='categorie',
        ),
    ]