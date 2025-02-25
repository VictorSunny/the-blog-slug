from django.shortcuts import render, redirect
from django.http import HttpResponse


def handler404(request, exception):
    # return HttpResponse("oops")
    return render(request, "404.html")

def handler500(request):
    return render(request, "404.html")

