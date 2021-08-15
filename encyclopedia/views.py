from django import forms
from django.shortcuts import redirect, render
from . import util

import encyclopedia
import markdown2
from random import randint

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": "Error",
            "content": "The requested page was not found."
        })

def search(request):
    q = request.GET['q']
    content = util.get_entry(q)
    if content is not None:
        return redirect("entry", title=q)
    else:
        result = []
        for entry in util.list_entries():
            if q.lower() in entry.lower():
                result.append(entry)
        return render(request, "encyclopedia/index.html", {
        "entries": result
        })

def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                "title": "Error",
                "content": "This entry already exists."
                })
            else:
                util.save_entry(title, content)
                return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/create.html")

def edit(request, entry):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(entry, content)
        return redirect("entry", title=entry)
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": entry,
            "content": util.get_entry(entry)
        })

def random(request):
    entries = util.list_entries()
    rnd_entry = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=rnd_entry)