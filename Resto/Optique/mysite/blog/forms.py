
from django import forms
from .models import Facture, Client

class FactureForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)
    numero = forms.CharField(max_length=10, required=False)  
    avance = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    CHOICES = [
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ]

    choix_avance = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Facture
        fields = ['client', 'article', 'quantite', 'prix_unitaire', 'numero']  



class ArticleSearchForm(forms.Form):
    min_price = forms.DecimalField(label="Prix minimum", required=False)
    max_price = forms.DecimalField(label="Prix maximum", required=False)
    start_date = forms.DateField(label="Date de début", required=False)
    end_date = forms.DateField(label="Date de fin", required=False)
