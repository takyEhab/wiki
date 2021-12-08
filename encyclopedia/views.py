from django import forms
from django.forms.widgets import Textarea
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import random
import markdown2
from . import util


class CreateNewEntry(forms.Form):
    TitleEntry = forms.CharField()
    Entry = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    entryMarkdown = markdown2.markdown(util.get_entry(entry))
    if entry.lower() in (string.lower() for string in util.list_entries()):
        return render(request, "encyclopedia/wiki.html", {
            "title": entry,
            "entry": entryMarkdown
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No entry found" 
        })

def search(request):
    q = (request.GET.get('q', '')).lower()
    if q in (string.lower() for string in util.list_entries()):
        return HttpResponseRedirect(reverse('wiki', kwargs={'entry': q}))

    elif (any(q in string for string in (string.lower() for string in util.list_entries()))):
        strings_with_substring = [string for string in (string.lower() for string in util.list_entries()) if q in string]
        return render(request, "encyclopedia/search.html", {
            "entries": strings_with_substring
        })
    return render(request, "encyclopedia/error.html", {
            "message": "No entry found" 
        })


def newpage(request):
    if request.method == "POST":
        form = CreateNewEntry(request.POST)

        if form.is_valid():
            title = form.cleaned_data["TitleEntry"]
            entry = form.cleaned_data["Entry"]

            if title.lower() in (string.lower() for string in util.list_entries()):
                return render(request, "encyclopedia/error.html", {
                    "message": "The title Already Exists"
                })

            util.save_entry(title, entry)
    
            return HttpResponseRedirect(reverse('wiki', kwargs={'entry': title}))

        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })


    return render(request, "encyclopedia/newpage.html", {
        "form": CreateNewEntry()
    })

def edit(request, entry):
    if request.method == "POST":
        if request.POST.get('entry'):
            util.save_entry(entry, request.POST.get('entry'))

            return HttpResponseRedirect(reverse('wiki', kwargs={'entry': entry}))
            
    return render(request, "encyclopedia/edit.html", {
        "title": entry,
        "entry": util.get_entry(entry)
    })

def rand(request):
    return HttpResponseRedirect(reverse('wiki', kwargs={'entry': random.choice(util.list_entries())}))