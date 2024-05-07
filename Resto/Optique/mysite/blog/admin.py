from django.contrib import admin
from . import models

admin.site.register(models.Article)
admin.site.register(models.Provider)
admin.site.register(models.Client)
admin.site.register(models.Stock)
admin.site.register(models.Commande)
admin.site.register(models.HistCommande)