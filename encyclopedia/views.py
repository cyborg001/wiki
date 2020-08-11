from django.shortcuts import render, redirect
from django import forms
import markdown2 as mk
import html
from . import util

class MyForm(forms.Form):
    q = forms.CharField()


def index(request):
    form = MyForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['q']
            if name in util.list_entries():
                return redirect(f'/wiki/{name}')
            else:
                l = []
                for n in util.list_entries():
                    if name in n:
                        l.append(n)
                print(l)
                if l:
                    return render(request,'encyclopedia/index.html',{
                        'entries':l,
                        'form':MyForm()
                    })

        else:
            return render(request,'encyclopedia/index.html',{
                'form':form
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form':MyForm()
    })

def wiki(request,name):
    form = MyForm()
    if name not in util.list_entries():
        return render(request, 'encyclopedia/wiki.html', {
            'entry':f'Error the {name} page was not found.',
            'name':'Error',
            'form':form,
        })
    entry = mk.markdown(util.get_entry(name))
    return render(request, 'encyclopedia/wiki.html', {
        'entry':entry,
        'name':name,
        'form':form,
    })
