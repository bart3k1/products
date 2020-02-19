from django.shortcuts import render


def home(request):
    return render(request, "prod_app/home.html")
