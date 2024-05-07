from multiprocessing import Value
from os import name
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.models import Commande, HistCommande, Provider, Article, Client, Stock, Facture
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import F
from django.db.models import Sum,Count
from django.db.models import Q
from .forms import FactureForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image




def home(request):
    return redirect("login")


def login(request):
    return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")

def accueil(request):
    return render(request, 'blog/accueil.html')

def provider(request):
    search = request.GET.get("search", "")
    list_provider = Provider.objects.all()

    if search:
        list_provider = list_provider.filter(
            Q(ville__icontains=search) | Q(raison_sociale__icontains=search) | Q(montant__icontains=search)
        )

    context = {
        "search": search,
        "list_provider": list_provider,
    }

    return render(request, "blog/provider.html", context)



def client(request):
    list_client = Client.objects.all().order_by("-name")
    return render(request, "blog/client.html", {"listclient": list_client})


def article(request):
    listarticle = Article.objects.all().order_by("-name")
    return render(request, "blog/article.html", {"listarticle": listarticle})


def stock(request):
    search = request.GET.get("search", "")
    if search != "":
        stock_list = Stock.objects.filter(name__icontains=search)
    else:
        stock_list = Stock.objects.all()

    context = {
        "search": search,
        "stock_list": stock_list,
    }
    return render(request, "blog/stock.html", context)




def edit_provider(request, provide_id):
    current_provider = Provider.objects.get(id=provide_id)
    if request.method == "POST":
        raison_sociale = request.POST.get("raison_sociale")
        name = request.POST.get("name")
        address = request.POST.get("address")
        ville = request.POST.get("ville")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")
        fix = request.POST.get("fix")
        email = request.POST.get("email")
        montant = request.POST.get("montant")
        if raison_sociale!= "" and name != "" and address != "" and ville != "" and zip_code != "" and phone != "" and fix != "" and email != "" and montant != "":
            current_provider.raison_sociale = raison_sociale
            current_provider.name = name
            current_provider.address = address
            current_provider.ville = ville
            current_provider.zip_code = zip_code
            current_provider.phone = phone
            current_provider.fix = fix
            current_provider.email = email
            current_provider.montant = montant
            current_provider.save()
            return redirect("/provider")
        else:
            messages.error(request, "Please fill in all the fields.")
            return redirect("edit_provider", provide_id=provide_id)
    else:
        return render(request, "blog/edit_provider.html", {"provider": current_provider})

def edit_client(request, client_id):
    current_client = Client.objects.get(id=client_id)
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        email = request.POST.get("email")
        zip_code = request.POST.get("zip_code")
        benificiaire = request.POST.get("benificiaire")
        monture = request.POST.get("monture")
        verre = request.POST.get("verre")
        phone = request.POST.get("phone")
        OG = request.POST.get("OG")
        OD = request.POST.get("OD")
        EIP = request.POST.get("EIP")
        ADD = request.POST.get("ADD")

        if name != "" and address != "" and email !="" and zip_code != "" and benificiaire != "" and monture != "" and verre != "" and phone != "" and OG != "" and OD != "" and EIP != "" and ADD != "":
            current_client.name = name
            current_client.address = address
            current_client.email = email
            current_client.zip_code = zip_code
            current_client.benificiaire = benificiaire
            current_client.phone = phone
            current_client.monture = monture
            current_client.verre = verre
            current_client.OG = OG
            current_client.OD = OD
            current_client.EIP = EIP
            current_client.ADD = ADD
            current_client.save()
            return redirect("/client")
        else:
            messages.error(request, "Please fill in all the fields.")
            return redirect("edit_client", client_id=client_id)
    else:
        return render(request, "blog/edit_client.html", {"client": current_client})

def new_provider(request):
    if request.method == "POST":
        raison_sociale = request.POST.get("raison_sociale")
        name = request.POST.get("name")
        address = request.POST.get("address")
        ville = request.POST.get("ville")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")
        fix = request.POST.get("fix")
        email = request.POST.get("email")
        montant = request.POST.get("montant")

        if not raison_sociale or not name or not address or not ville or not zip_code or not phone or not fix or not email or not montant:
            messages.error(request, "Please fill in all fields.")
            return redirect("new_provider")

        # Check if a provider with the same information already exists
        if Provider.objects.filter(
            raison_sociale=raison_sociale, name=name, address=address, ville=ville, zip_code=zip_code, phone=phone, montant=montant, email=email
        ).exists():
            messages.error(
                request, "A Provider with the same information already exists."
            )
            return redirect("new_provider")
        elif Provider.objects.filter(phone=phone).exists():
            messages.error(
                request, "A Provider with the same phone number already exists."
            )
            return redirect("new_provider")
        elif Provider.objects.filter(name=name).exists():
            messages.error(request, "A Provider with the same name already exists.")
            return redirect("new_provider")

        current_provider = Provider(
            raison_sociale=raison_sociale,
            name=name,
            address=address,
            ville=ville,
            zip_code=zip_code,
            phone=phone,
            fix=fix,
            email=email,
            montant=montant,
        )
        current_provider.save()
        return redirect("provider")  # Redirect to the providers page after successfully adding the provider
    else:
        return render(request, "blog/new_provider.html")



def new_client(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        email = request.POST.get("email")
        zip_code = request.POST.get("zip_code")
        benificiaire = request.POST.get("benificiaire")
        monture = request.POST.get("monture")
        verre = request.POST.get("verre")
        phone = request.POST.get("phone")
        OG = request.POST.get("OG")
        OD = request.POST.get("OD")
        EIP = request.POST.get("EIP")
        ADD = request.POST.get("ADD")
        if not name or not address or not email or not zip_code or not benificiaire or not monture or not verre or not phone or not OG or not OD or not EIP or not ADD :
            messages.error(request, "Please fill in all fields.")
            return redirect("new_client")

        # Check if a client with the same information already exists
        if Client.objects.filter(
            name=name, address=address, email=email, zip_code=zip_code, benificiaire=benificiaire, phone=phone, OG=OG, OD=OD  
        ).exists():
            messages.error(
                request, "A client with the same information already exists."
            )
            return redirect(
                "new_client"
            )  # Redirect to the new_client page with error message
        elif Client.objects.filter(phone=phone).exists():
            messages.error(
                request, "A client with the same phone number already exists."
            )
            return redirect("new_client")
        elif Client.objects.filter(name=name).exists():
            messages.error(request, "A client with the same name already exists.")
            return redirect("new_client")
        current_client = Client(
            name=name, address=address, email=email, zip_code=zip_code, benificiaire=benificiaire,  phone=phone, OG = OG, OD = OD 
        )
        current_client.save()
        return redirect(
            "client"
        )  # Redirect to the clients page after successfully adding the client
    else:
        return render(request, "blog/new_client.html")


def new_article(request):
    if request.method == "POST":
        name = request.POST.get("name")
        reference = request.POST.get("reference")
        categorie = request.POST.get("categorie")
        price = request.POST.get("price")
        barcode = request.POST.get("barcode")
        quantite = request.POST.get("quantite")
        provider_id = request.POST.get("provider")

        if not name or not reference or not categorie or not price or not barcode or not quantite:
            messages.error(request, "Please fill in all fields.")
            return redirect("new_article")

        elif Article.objects.filter(barcode=barcode).exists():
            messages.error(request, "An article with the same barcode already exists.")
            return redirect("new_article")
        current_article = Article(
            name=name, reference=reference, categorie=categorie, price=price, barcode=barcode, quantite=quantite
        )
        if provider_id:
            current_article.provider_id = provider_id
        current_article.save()

        if Stock.objects.filter(name=current_article.name).exists():
            stock = Stock.objects.get(name=current_article.name)
            stock.stock = stock.stock + int(current_article.quantite)
            stock.save()
        elif not Stock.objects.filter(name=current_article.name).exists():
            Stock.objects.create(
                article=current_article,
                stock=current_article.quantite,
                name=current_article.name,
            )
        return HttpResponseRedirect("/article")
    else:
        list_provider = Provider.objects.all().order_by("-name")
        return render(
            request, "blog/new_article.html", {"list_provider": list_provider}
        )

def edit_article(request, article_id):
    current_article = Article.objects.get(id=article_id)
    list_provider = Provider.objects.all().order_by("-raison_sociale")
    if request.method == "POST":
        name = request.POST.get("name")
        reference = request.POST.get("reference")
        categorie = request.POST.get("categorie")
        price = request.POST.get("price")
        barcode = request.POST.get("barcode")
        quantite = request.POST.get("quantite")
        provider_id = request.POST.get("provider")

        if name != "" and reference != "" and categorie != "" and price != "" and barcode != "" and quantite != "" and provider_id != "":
            current_article.name = name
            current_article.reference = reference
            current_article.categorie = categorie
            current_article.price = price
            current_article.barcode = barcode
            current_article.quantite = quantite
            current_article.provider = Provider.objects.get(id=provider_id)
            current_article.save()
            return redirect("/article")
        else:
            messages.error(request, "Please fill in all the fields.")
            return redirect("edit_article", article_id=article_id)
    else:
        return render( request,"blog/edit_article.html",
            {"article": current_article, "list_provider": list_provider},)

def delete_provider(request, provide_id):
    Provider.objects.get(id=provide_id).delete()
    return HttpResponseRedirect("/provider")


def delete_client(request, client_id):
    Client.objects.get(id=client_id).delete()
    return HttpResponseRedirect("/client")


def delete_article(request, article_barcode):
    try:
        article = Article.objects.get(barcode=article_barcode)
        stock = Stock.objects.get(name=article)
        stock.stock -= article.quantite
        stock.save()
        article.delete()
    except Stock.DoesNotExist:
        pass
    return HttpResponseRedirect("/article")


def delete_stock(request, name):
    Stock.objects.get(name=name).delete()

    articles = Article.objects.filter(name=name)
    for article in articles:
        article.delete()

    return redirect("stock")


def vente(request):
    listeArticle = {}
    listkey = {}
    listClient = {}
    create_commande = False

    if request.method == "POST":
        name = request.POST.get("produit")
        quantite = int(request.POST.get("qty"))
        client_id = request.POST.get("client")
        if not name or not quantite or not client_id:
            # One or more required fields are missing
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                quantite = int(quantite)
                client_id = int(client_id)
                articles = Article.objects.filter(name=name)  # Use filter instead of get

                if articles.exists():
                    article = articles.first()  # Retrieve the first matching article
                    stock = Stock.objects.get(name=article.name)

                    if quantite > stock.stock:
                        messages.error(request, "Quantity exceeds the available stock")
                    else:
                        if "listkey" in request.session:
                            listkey = request.session.get("listkey")
                            listkey[article.name] = quantite

                        request.session["listkey"] = listkey
                        listClient["id"] = client_id
                        request.session["listClient"] = listClient
                        request.session["listkey"] = listkey
                        create_commande = True

                else:
                    messages.error(request, "Article does not exist!")

            except Article.DoesNotExist:
                messages.error(request, "Article does not exist!")

    if "listkey" not in request.session:
        request.session["listkey"] = listkey
    else:
        listkey = request.session["listkey"]

    if "listClient" not in request.session:
        request.session["listClient"] = listClient
    else:
        listClient = request.session["listClient"]

    if create_commande:
        try:
            for key, value in listkey.items():
                articles = Article.objects.filter(name=key)  # Use filter instead of get

                if articles.exists():
                    article = articles.first()  # Retrieve the first matching article
                    listeArticle[article.name] = [article, value]
                    Commande.objects.create(
                        article=article,
                        client=Client.objects.get(id=listClient["id"]),
                        quantite=value,
                    )
                    listkey = {}
                    request.session["listkey"] = listkey

                else:
                    messages.error(request, "Article does not exist!")

        except Article.DoesNotExist:
            messages.error(request, "Article does not exist!")

    clients = Client.objects.all()
    commandes = Commande.objects.all()
    articles = Article.objects.all()

    context = {
        "clients": clients,
        "commandes": commandes,
        "articles": articles,
        "listarticles": listeArticle,
        "listkey": listkey,
        "listClient": listClient,
    }
    return render(request, "blog/caisse.html", context)

def paiement(request):
    # Retrieve commands with multiple occurrences of the same article name
    duplicate_article_names = Commande.objects.values("article__name").annotate(
        name_count=Count("article__name")
    ).filter(name_count__gt=1)

    total_quantite = 0

    for duplicate_article in duplicate_article_names:
        article_name = duplicate_article["article__name"]
        total_quantite += Commande.objects.filter(article__name=article_name).aggregate(total=Sum("quantite"))["total"]

    try:
        commandes = Commande.objects.all()

        for commande in commandes:
            try:
                article = commande.article
                client = commande.client

                # Update stock quantity
                stock = Stock.objects.get(name=article.name)
                if stock.stock >= commande.quantite:
                    stock.stock -= commande.quantite
                    stock.save()
                else:
                    messages.error(request, f"Insufficient stock for {article.name}")

                # Create historical record
                HistCommande.objects.create(
                    article=article,
                    client=client,
                    quantite=commande.quantite,
                )

            except Article.DoesNotExist:
                messages.error(request, f"Article {article.name} does not exist")
            except Client.DoesNotExist:
                messages.error(request, f"Client with ID {client.id} does not exist")

        Commande.objects.all().delete()
        messages.success(request, "Payment and order processing successful.")
    except Exception as e:
        messages.error(request, f"Error during payment and order processing: {str(e)}")

    return redirect("caisse")


def delete_all_articles(request, commande_id):
    Commande.objects.get(id=commande_id).delete()

    return HttpResponseRedirect("/caisse")


def historique_commande(request):
    search = request.GET.get("search", "")
    if search != "":
        hist_commandes = HistCommande.objects.filter(article__name__icontains=search)
    else:
        hist_commandes = HistCommande.objects.all()

    context = {
        "search": search,
        "hist_commandes": hist_commandes,
    }
    return render(request, "blog/historique_commande.html", context)

def delete_commande(request, commande_id):
    try:
        commande = HistCommande.objects.get(id=commande_id)
        commande.delete()
        messages.success(request, "Commande supprimée avec succès.")
    except HistCommande.DoesNotExist:
        messages.error(request, "La commande spécifiée n'existe pas.")
    
    return redirect("historique")




from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
from decimal import Decimal

def generate_facture_pdf(facture):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Define custom paragraph styles
    styles = getSampleStyleSheet()
    custom_heading_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.darkblue,
    )
    custom_normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        textColor=colors.black,
    )

    montant_ht = Decimal(facture.quantite) * Decimal(facture.prix_unitaire)
    tva = Decimal('0.20')
    montant_tva = montant_ht * tva
    montant_ttc = montant_ht + montant_tva

    # Tableau de données pour la facture
    data = [
        ['Facture N°', facture.numero],
        ['Client', facture.client.name],
        ['Article', facture.article.name],
        ['Quantité', str(facture.quantite)],
        ['Prix unitaire', "{:.2f} DH".format(facture.prix_unitaire)],
        ['Montant HT', "{:.2f} DH".format(montant_ht)],
        ['TVA ({:.0%})'.format(tva), "{:.2f} DH".format(montant_tva)],
        ['Montant TTC', "{:.2f} DH".format(montant_ttc)]
    ]

    # Définir un style pour le tableau
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('LEADING', (0, 0), (-1, -1), 15),
        ('BACKGROUND', (0, -2), (-1, -2), colors.lightblue),  # Avance
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgreen),  # Montant Restant
    ])

    # Créer les éléments pour la facture
    elements = []

    # Create a container table for the logo and header text
    header_table_data = [
        [Image("https://digiup.ma/wp-content/uploads/2020/12/Capture_d_ecran_2022-08-26_153120-removebg-preview.png", width=120, height=70), Paragraph("DIGI OPTIQUE ", custom_heading_style)],
        [None, Paragraph("Adresse : 9 Rue Figuig, Rabat 10000, Maroc", custom_normal_style)],
        [None, Paragraph("Téléphone : +212 661-841242", custom_normal_style)],
        # Add the date to the header table
        [None, Paragraph("Date : {}".format(facture.date), custom_normal_style)] if facture.date else None,
        # Add a spacer for separation
        [None, Spacer(1, 24)],
    ]

    # Remove None values from the header_table_data list
    header_table_data = [row for row in header_table_data if row is not None]

    # Set the widths of columns to adjust the position of logo and paragraph
    header_table = Table(header_table_data, colWidths=[350, 120], rowHeights=[20, 20, 20, 20, 24])
    header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))  # Align the elements to the middle

    # Add the header table to the elements list
    elements.append(header_table)

    # Ajouter le titre de la facture avec une mise en forme appropriée
    elements.append(Paragraph("Facture", custom_heading_style))
    elements.append(Spacer(1, 12))

    # Créer le tableau
    table = Table(data, colWidths=120, rowHeights=30)
    table.setStyle(table_style)

    # Ajouter le tableau au PDF
    elements.append(table)

    # Ajouter l'avance et le montant restant s'ils sont disponibles
    if facture.avance:
        avance = Decimal(facture.avance)
        montant_restant = montant_ttc - avance

        avance_table_data = [
            ['Avance', "{:.2f} DH".format(avance)],
            ['Montant Restant', "{:.2f} DH".format(montant_restant)],
        ]

        avance_table = Table(avance_table_data, colWidths=120, rowHeights=30)
        avance_table.setStyle(table_style)

        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Avance et Montant Restant :", custom_heading_style))
        elements.append(Spacer(1, 6))
        elements.append(avance_table)

    # Ajouter les informations de paiement
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Informations de paiement :", custom_heading_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("IBAN : XXXX XXXX XXXX XXXX XXXX", custom_normal_style))
    elements.append(Paragraph("BIC/SWIFT : XXXXXXXX", custom_normal_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Veuillez effectuer le paiement avant la date d'échéance indiquée sur la facture.", custom_normal_style))

    # Créer le PDF
    pdf.build(elements)

    buffer.seek(0)
    return buffer







def creer_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            # Get the 'numero' value from the form data
            numero_facture = form.cleaned_data['numero']

            # Save the 'facture' object with the 'numero' value
            facture = form.save(commit=False)
            facture.numero = numero_facture

            # Save the 'avance' value if provided by the user
            choix_avance = form.cleaned_data['choix_avance']
            if choix_avance == 'Oui':
                facture.avance = form.cleaned_data['avance']
            else:
                facture.avance = None

            facture.save()

            pdf_buffer = generate_facture_pdf(facture)
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'filename=facture.pdf'
            return response

    else:
        form = FactureForm()

        # Remove 'required' attribute from the avance field if 'Non' is selected for choix_avance
        if 'choix_avance' in request.GET and request.GET['choix_avance'] == 'Non':
            form.fields['avance'].required = False
        else:
            form.fields['avance'].required = True

    return render(request, 'blog/creer_facture.html', {'form': form})



from django.db.models import Sum

def rapport_annuel(request):
    fournisseurs = Provider.objects.all()
    clients = Client.objects.all()
    articles = Article.objects.all()

    fournisseurs_montants = [f.montant for f in fournisseurs]
    clients_montants = [c.facture_set.aggregate(Sum('prix_unitaire'))['prix_unitaire__sum'] for c in clients]

    context = {
        'fournisseurs': fournisseurs,
        'clients': clients,
        'articles': articles,
        'fournisseurs_montants': fournisseurs_montants,
        'clients_montants': clients_montants,
    }
    return render(request, 'blog/rapport_annuel.html', context)











