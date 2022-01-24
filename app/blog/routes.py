from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import current_user, login_required
from .forms import CreatePostForm
from app.models import Post

blog = Blueprint('blog',__name__,template_folder='blog_templates')

from app.models import db
import requests as r
from app.models import Pokemon

@blog.route('/')
def blogHome():
    posts = Post.query.all()
    return render_template('blog.html' , posts = posts)

@blog.route('/pokebikes')
def pokeBikes():
    data = r.get('https://pokeapi.co/api/v2/item/bicycle/')
    my_data = data.json()
    bikes = [dict['name'] for dict in my_data['names']]
    my_img = my_data['sprites']['default']
    return render_template('pokebikes.html', bikes = bikes, my_img = my_img)


@blog.route('/posts/create', methods=["GET","POST"])
@login_required
def createPost():
    form = CreatePostForm()
    if request.method == "POST":
            if form.validate():
                print('form was validated')
                title = form.title.data
                image = form.image.data
                content = form.content.data

            
                post = Post(title, image, content, current_user.id)
                db.session.add(post)
                db.session.commit()
            
                return redirect(url_for('blog.blogHome'))

    return render_template('createpost.html', form=form)

@blog.route('/search/pokemon', methods=['POST'])
def searchPokemon():
    if request.method == "POST":
        print('request is made')
        my_pokemon = request.form['poke']
        data = data = r.get(f'https://pokeapi.co/api/v2/pokemon/{my_pokemon}')
        if data.status_code == 200:
            my_data = data.json()
            
            pokemon = {
                'name':'',
                'image':'',
                'types': [],
            }
            for type in my_data['types']:
                pokemon['types'].append(type['type']['name'])
            pokemon['name'] = my_data['name']
            pokemon['image'] = my_data['sprites']['front_default']

            name = pokemon['name']
            image = pokemon['image']
            types = pokemon['types']

            pk = Pokemon(name,image,types)

            db.session.add(pk)

            db.session.commit()
            
            return render_template('pokemon.html', pokemon = pokemon)
        else:
            pokemon = ''
            return render_template('pokemon.html', pokemon = pokemon)

    
    return {'hello':'you'}