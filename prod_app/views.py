from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product, Votes


def home(request):
    products = Product.objects.all().order_by("-votes_total")
    return render(request, "prod_app/home.html", {"products": products})


@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == "POST":
        if request.POST["title"] and request.POST["body"] and request.POST["url"] and request.FILES["icon"] and request.FILES["image"]:
            product = Product()
            product.title = request.POST["title"]
            product.body = request.POST["body"]
            if request.POST["url"].startswith("http://") or request.POST["url"].startswith("https://"):
                product.url = request.POST["url"]
            else:
                product.url = "http://" + request.POST["url"]
            product.icon = request.FILES["icon"]
            product.image = request.FILES["image"]
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            #todo redirect to product deteails
            return redirect("/products/" + str(product.id))

        else:
            return render(request, "prod_app/create", {"error": "All fields are required"})

    else:
        return render(request, "prod_app/create.html")


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    return render(request, "prod_app/detail.html", {"product": product})


@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == "POST":
        if Votes.objects.filter(user=request.user.id, product=product_id).exists():
            return redirect("/products/"+str(product_id))
        else:
            product = get_object_or_404(Product, pk=product_id)
            product.votes_total += 1
            product.save()
            Votes(product=product, user=request.user).save()
            return render(request, "prod_app/detail.html", {"product": product})

    return redirect("/products/"+str(product_id))

