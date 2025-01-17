# Generated by Django 4.2.1 on 2023-07-14 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_client_degree'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('cin_ice', models.CharField(default='', max_length=100)),
                ('type', models.CharField(choices=[('client', 'Client'), ('fournisseur', 'Fournisseur')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
