from django.db import models

DEFAULT_ID = 1

class Provider(models.Model):
    raison_sociale = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    fix = models.CharField(max_length=50, default="")
    address = models.TextField()
    ville = models.CharField(max_length=50, default="")
    zip_code = models.CharField(max_length=10, default="")
    email = models.EmailField(max_length=254)
    montant = models.DecimalField(decimal_places=2, max_digits=10)
    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    address = models.TextField()
    email = models.EmailField(max_length=254, default="")
    zip_code = models.CharField(max_length=10, default="")
    benificiaire = models.CharField(max_length=50, default="")
    monture = models.CharField(max_length=50, default="")
    verre = models.CharField(max_length=50, default="")
    OG = models.CharField(max_length=10, default="")
    OD = models.CharField(max_length=10, default="")
    EIP = models.CharField(max_length=50, default="")
    ADD = models.CharField(max_length=50, default="")
    
    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=500, default="")
    reference = models.CharField(max_length=500, default="")
    categorie = models.CharField(max_length=500, default="")
    price = models.FloatField()
    barcode = models.IntegerField()
    quantite = models.IntegerField(default=0)
    provider = models.ForeignKey(
        "Provider", on_delete=models.CASCADE, default=DEFAULT_ID
    )

    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    name = models.CharField(default=article.name, max_length=500)
    stock = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Commande(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    quantite = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.article.name


class HistCommande(models.Model):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    quantite = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return f"HistCommande object (id: {self.id})"
    


class Facture(models.Model):
    TYPE_CHOICES = (
        ('C', 'Client'),
        ('F', 'Fournisseur'),
    )
    numero = models.CharField(max_length=10, default="")
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    fournisseur = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    avance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"Facture object (id: {self.id})"



