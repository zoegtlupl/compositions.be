from flask import Flask, send_from_directory, render_template
from flask_flatpages import FlatPages
import os
import random

FLATPAGES_EXTENSION = '.md'
FLATPAGES_AUTO_RELOAD = True

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/atlas-programation'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FLATPAGES_MARKDOWN_EXTENSIONS = ['extra']
FLATPAGES_EXTENSION_CONFIGS = {
    'codehilite': {'linenums': 'True'}
}

app.config.from_object(__name__)
pages = FlatPages(app)

def Liste_cat():
    articles = (p for p in pages if 'published' in p.meta)
    catList = set()
    for a in articles:
        if 'cat' in a.meta:
            catList.add(a.meta['cat'])
    return list(catList)

def Liste_cat_by_author(author_name):
    articles = (p for p in pages if 'published' in p.meta and 'author' in p.meta and p.meta['author'] == author_name)
    catList = set()
    for a in articles:
        if 'cat' in a.meta:
            catList.add(a.meta['cat'])
    return list(catList)

def Liste_authors():
    desired_order = ["vendredi", "samedi", "dimanche"]
    articles = (p for p in pages if 'published' in p.meta and 'author' in p.meta)
    authorsList = set()
    for a in articles:
        if 'author' in a.meta:
            authorsList.add(a.meta['author'])
    authorsList = list(authorsList)
    
    # Debugging: Print authors list before sorting
    print("Authors before sorting:", authorsList)
    
    authorsList.sort(key=lambda x: desired_order.index(x.lower()) if x.lower() in desired_order else len(desired_order))
    
    # Debugging: Print authors list after sorting
    print("Authors after sorting:", authorsList)
    
    return authorsList

def imagelist(articlename):
    dir_path = os.path.join(BASE_DIR, 'pages', articlename)
    if os.path.exists(dir_path):
        images = [f for f in os.listdir(dir_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg'))]
        images = ["pages/" + articlename + "/" + img for img in images]
        return articlename, images
    else:
        return None, None

def get_random_image():
    images_dir = os.path.join(BASE_DIR, 'static', 'img', 'home-image')
    images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg'))]
    if images:
        return 'img/home-image/' + random.choice(images)
    else:
        return 'img/default.png'

@app.route('/<path:path>')
def page(path):
    try:
        page = pages.get_or_404(path)
        
        # Déterminer le nom du fichier CSS en fonction de la catégorie
        css_file = page.meta.get('cat', 'default') + '.css'
        css_path = os.path.join(BASE_DIR, 'static', css_file)
        if not os.path.exists(css_path):
            css_file = 'default.css'
        
        catList = Liste_cat()
        authorsList = Liste_authors()
        g_path, imgs = imagelist(path)
        selectedAuthor = page.meta.get('author', '')
        selectedcat = page.meta.get('cat', '')
        articles = [p for p in pages if 'published' in p.meta]
        
        if imgs:
            return render_template('single.html', 
                                   page=page, 
                                   catList=catList, 
                                   authorsList=authorsList, 
                                   g_path=g_path, 
                                   imgs=imgs, 
                                   selectedAuthor=selectedAuthor, 
                                   selectedcat=selectedcat, 
                                   articles=articles,
                                   css_file=css_file)
        else:
            return render_template('single.html', 
                                   page=page, 
                                   catList=catList, 
                                   authorsList=authorsList, 
                                   selectedAuthor=selectedAuthor, 
                                   selectedcat=selectedcat, 
                                   articles=articles,
                                   css_file=css_file)
    except Exception as e:
        return str(e), 500

@app.route('/info')
def info():
    try:
        page = pages.get_or_404('info')
        catList = Liste_cat()
        return render_template('staticpage.html', page=page, catList=catList)
    except Exception as e:
        return str(e), 500

@app.route('/cat/<path:catname>')
def catPage(catname):
    try:
        articles = (p for p in pages if 'published' in p.meta and 'cat' in p.meta and p.meta['cat'] == catname)
        latest = sorted(articles, reverse=True, key=lambda p: p.meta['published'])
        catList = Liste_cat()
        authorsList = Liste_authors()
        selectedcat = catname
        return render_template('cat.html', articles=latest, catList=catList, authorsList=authorsList, selectedcat=selectedcat)
    except Exception as e:
        return str(e), 500

@app.route('/author/<path:authorname>')
def authorPage(authorname):
    try:
        author_names = authorname.split('+')
        articles = [p for p in pages if 'published' in p.meta and 'author' in p.meta and p.meta['author'] in author_names]
        latest = sorted(articles, reverse=True, key=lambda p: p.meta['published'])
        catList = Liste_cat_by_author(author_names[0])
        authorsList = Liste_authors()
        selectedAuthor = authorname
        return render_template('author.html', articles=latest, catList=catList, authorsList=authorsList, selectedAuthor=selectedAuthor)
    except Exception as e:
        return str(e), 500

@app.route('/pages/<path:path>')
def serve_pages(path):
    return send_from_directory('pages', path)

@app.route('/')
def index():
    try:
        random_image = get_random_image()
        articles = (p for p in pages if 'published' in p.meta)
        latest = sorted(articles, reverse=True, key=lambda p: p.meta['published'])
        catList = Liste_cat()
        authorsList = Liste_authors()
        return render_template('index.html', articles=latest, catList=catList, authorsList=authorsList, random_image=random_image)
    except Exception as e:
        return str(e), 500

@app.errorhandler(404)
def page_not_found(e):
    return "Problem", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
