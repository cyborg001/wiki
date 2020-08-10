from django.shortcuts import render
from django import forms
from . import util

class MyForm(forms.Form):
    q = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request):
    return render(request, "encyclopedia/entry.html", {})
    pass
