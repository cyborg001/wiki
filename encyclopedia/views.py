from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
import markdown2 as mk
import html
import random
from .forms import MyForm, NewPageForm
from . import util
import re


def index(request):
    '''si el metodo es POST y los datos son validos investiga si la wiki
        digitada existe, si existe nos redirecciona a ella, sino nos envia
        una lista con todas las wikis cuyo nombre contegan la substring
        digitada. por otro lado si el metodo es GET entonces nos envia a
        una lista con todas las wikis existentes'''

    form = MyForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['Entry']
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
    '''esta funcion que acepta request y a name como parametro se
        asegura de devolver la wiki en formato html para que pueda ser
        visualizada por los usuarios. si la wiki no existe devuelve
        un error diciendo que la wiki no fue encontrada'''

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

def random_page(request):
    '''Esta funcion devuelve una wiki aleatoria de las existentes  '''

    num = random.randint(0,len(util.list_entries())-1)
    return redirect(f'wiki/{util.list_entries()[num]}')

def new_page(request):
    '''Esta funcion nos permite crear nuestra propia wiki, llenando un titulo
        para el titulo de la pagina y un contenido en formato Markdown para que
        el creador pueda desarrollar contenido mucho mas facil y rapido
        aqui pueden ir a una pagina acerca de este formato:
        https://docs.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax'''

    form  = MyForm()
    newPageForm = NewPageForm(request.POST)
    if request.method == 'POST':
        if newPageForm.is_valid():
            title = newPageForm.cleaned_data['title']
            content = newPageForm.cleaned_data['content']
            if title in util.list_entries():
                return render(request, 'encyclopedia/new_page.html', {
                    'form':form,
                    'newPageForm':newPageForm,
                    'error':'Error the entry already exists!',
                })
            else:
                util.save_entry(title,content)
                return redirect(f'/wiki/{title}')
    return render(request, 'encyclopedia/new_page.html', {
        'form':form,
        'newPageForm':NewPageForm()
    })

def edit(request):
    '''Esta funcion nos permite editar una pagina visitada dandole al link
        "click hera for edit page" nos permite ir a una pagina para la ediccion
        de nuestra wiki'''
        
    print(request.POST)
    form = MyForm()
    newPageForm = NewPageForm(request.POST)
    if request.method == 'POST':
        if newPageForm.is_valid():
            title = newPageForm.cleaned_data['title']
            content = newPageForm.cleaned_data['content']
            util.save_entry(title,content)
            return redirect(f'/wiki/{title}')

    referencia = request.headers['Referer']
    t = re.findall('[^(https://127.0.0.1:8000/wiki/)]\w*',referencia)[-1]
    c = util.get_entry(t)
    request.POST ={'title':t,'content':c}
    print(request.POST)
    return render(request, 'encyclopedia/edit.html', {
        'form': form,
        'newPageForm':NewPageForm(request.POST),
        'error':'',
    })
