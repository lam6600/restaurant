# Generated by Django 4.2.1 on 2023-07-16 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_delete_facture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField()),
                ('prix_unitaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.client')),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.provider')),
            ],
        ),
    ]
