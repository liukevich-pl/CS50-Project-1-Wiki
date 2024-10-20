import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

#FIX replace space with underscore - for pages with more than 1 word in the title
def get_url(title):
    return title.replace(" ","_").strip()

#FIX replace underscore with space - for pages with more than 1 word in the title
def get_title(url):
    return url.replace("_"," ").strip()

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    entries = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))
    return entries

def list_urls():
    entries = list_entries()
    array = []
    for val in entries:
        array.append('<a href="/wiki/'+val+'">'+get_title(val)+'</a>')
    return array


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{get_url(title)}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

# Delete entry
def delete_entry(url):
    try:
        f = default_storage.delete(f"entries/{url}.md")
        return f
    except FileNotFoundError:
        return None
    
# Check contain key 
def search_check(filename, key):
    filename = filename.lower()
    key = key.lower()
    check = False
    if(key in filename):
        check = True
    return check

# Search list
def search_list_entries(key):
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md") and search_check(filename,key)))

# Edit data func
def edit_data(url,content,request):
    data = {}
    # Set default
    data["title"] = get_title(url)
    data["url"] = url
    data["content"] = content
    data["msg"] = ""
    # Check POST 
    if request.POST:
        err = ''
        if(request.POST.get('title','')): 
            url = get_url(request.POST.get('title',''))
        content = request.POST.get('content','')
        if len(content) < 5:
            #min 5 characters
            err = 'The minimum Content length must be at least 5 characters.'
        if len(url) < 3 :
            # min 3 characters
            err = 'The minimum title length must be at least 3 characters.'
        if request.POST.get('title','') and get_entry(url):
            # if already exists with the provided title
            err = 'There is already such a page on the wiki'
        data["title"] = get_title(url)
        data["url"] = url
        data["content"] = content
        data["msg"] = err
        if err == '':
            #save if correct
            save_entry(url, content)
            #provide success
            data["success"] = url
    return data