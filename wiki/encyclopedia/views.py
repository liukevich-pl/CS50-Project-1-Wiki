
from django.http import HttpResponse
from django.shortcuts import redirect,render
from . import util
from markdown2 import Markdown
import random

# Index Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_urls()
    })

# Open Page
def open(request, url):
    page_content = util.get_entry(url)
    if page_content != None:
        # If isset page
        # Markdown to HTML
        html_content = Markdown().convert(page_content)
        # Get Title from text, not from the query
        if page_content == '': html_content = '<h1>'+util.get_title(url)+'</h1>'
        # Render
        return render(request, "encyclopedia/page.html", {
            "title": util.get_title(url),
            "url": url,
            "content": html_content
        })
    else:
        # If not found
        return render(request, "encyclopedia/error.html", {
            "title": util.get_title(url)
        })
    
# Search Page
def search(request):
    key = request.POST.get('q','')
    #FIX replace space with underscore - for pages with more than 1 word in the title
    key = key.replace(" ","_")
    # reduce text for title
    key_title = key if len(key) <= 10 else key[:10]+"..."
    if key != "":
        if util.get_entry(key):
            # if key = Page title
            return redirect('wiki/'+key)
        else:
            # if isset POST data - show Search result
            return render(request, "encyclopedia/search.html", {
                "title": 'Search results for key "'+key_title+'"',
                "entries": util.search_list_entries(key),
                "key": key
            })
    else:
        # if empty POST data - redirect to Home page 
        return redirect('index')

# Add Page
def add(request):
    url = ''
    content = ''
    data = util.edit_data(url,content,request);
    if "success" in data:
        return redirect('wiki/'+data["success"])
    return render(request, "encyclopedia/edit.html", {
        "title": 'Create new Page',
        "data": data,
        "action": {"url":"add", "btn":"Create"}
    })

# Edit Page
def edit(request, url):
    if util.get_entry(url):
        content = util.get_entry(url)
        data = util.edit_data(url,content,request);
        if "success" in data:
            return redirect('/wiki/'+data["success"])
        return render(request, "encyclopedia/edit.html", {
            "title": 'Edit Page"'+util.get_title(url)+'"',
            "data": data,
            "action": {"url":"/wiki/"+url+'/edit', "btn":"Save"}
        })
    else:
        return redirect('index')
    
# Delete Page 
def delete(request, url):
    util.delete_entry(url)
    return redirect('index')

# Random Page 
def random_page(request):
    list = util.list_entries()
    rand = random.randint(0, len(list) - 1)
    url = list[rand]
    return redirect('/wiki/'+url)