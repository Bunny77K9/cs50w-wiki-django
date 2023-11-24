from logging import PlaceHolder
from random import randrange
from turtle import title
from django.shortcuts import render
import markdown2
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util

class FormTitle(forms.Form):
    title = forms.CharField(label="",
    widget=forms.TextInput(attrs={'placeholder':'Enter title'}))

class FormContent(forms.Form):
    content = forms.CharField(label="",
    widget=forms.Textarea(attrs={'placeholder':'Enter content'}))

def index(request):

    search = []

    if request.method == "POST":
        query = request.POST['query']

        for title in util.list_entries():
            if query.lower() == title.lower():
                return wiki_title(request, title)
                
            if query.lower() in title.lower():
                search.append(title)
        if search != []: # all results with substring 
            return render(request, "encyclopedia/search.html", {
            "results":search
        })
        else: 
            return render(request, "encyclopedia/404.html", {
            "message1": "Looks new for me!",
            "message2": "Requested page was not found",
            "message3": "Create new Page"})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def wiki_title(request, title):

    if util.get_entry(title) is None:
        return render(request, "encyclopedia/404.html", {
            "message1": "Look like you're lost!",
            "message2": "Requested page was not found",
            "message3": "Go to Home"})
    else:
        return render(request, "encyclopedia/title.html", {
            "title":title.capitalize(),
            "entry":markdown2.markdown(util.get_entry(title)),
        })

def add(request):

    title_input = FormTitle(request.POST)
    content_input = FormContent(request.POST)

    if request.method == "POST":
        if title_input.is_valid() and content_input.is_valid():
            title = title_input.cleaned_data["title"]
            content = content_input.cleaned_data["content"]

            if util.get_entry(title) is not None:
                 return render(request, "encyclopedia/Page Exists.html", {
                "title":title})
            else:
                util.save_entry(title, '#' + title + '\n' + content)
                return wiki_title(request, title)
    else:
        return render(request, "encyclopedia/add.html", {
            "new_title": FormTitle(),
            "new_content": FormContent()
        })

def edit(request, title):

    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "text_edit": FormContent(initial={'content':content})
        })

    else:
        content_form = FormContent(request.POST)
        if content_form.is_valid():
            content = content_form.cleaned_data["content"]
            util.save_entry(title, content)
            return wiki_title(request, title)

def random(request):
    
    index = randrange(len(util.list_entries()))
    return wiki_title(request, util.list_entries()[index])