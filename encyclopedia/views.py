from django.shortcuts import render
from django import forms
import markdown2 as mk
import html
from . import util

class MyForm(forms.Form):
    q = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def wiki(request,name):
    if name not in util.list_entries():
        return render(request, 'encyclopedia/wiki.html', {
            'entry':f'Error the {name} page was not found.',
            'name':'Error'
        })
    entry = mk.markdown(util.get_entry(name))
    return render(request, 'encyclopedia/wiki.html', {
        'entry':entry,
        'name':name,
    })
# def entry(request):
#     return render(request, "encyclopedia/entry.html", {})
#     pass
