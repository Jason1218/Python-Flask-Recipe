from flask import Flask, jsonify, request, render_template, url_for, session, redirect
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_required
from flask_jwt import JWT
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,DateTimeField,TextField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'jason'
login = LoginManager(app)
app.config['SECRET_KEY']== 'jason'
recipes = [{'name': 'lasagna', 'date added': '3/16/2019','ingredients': ['cheese', 'tomato sauce', 'ground beef'], 
'serving size': '2 people'},{'name': 'pizza'}]

class DeleteForm(FlaskForm):
    name = StringField("What recipe would you like to delete?")
    submit = SubmitField('Submit')

class InfoForm(FlaskForm):
    name = StringField("What is the name of the recipe?")
    ingredients = StringField("What are the ingredients involved?")
    instructions = StringField("What are the instructions to make this recipe?")
    servingSize = StringField("What is the serving size?")
    category = StringField("What type of food is this?")
    notes = StringField("Enter any notes here")
    dateAdded = StringField("Date added")
    dateModified = StringField("Date modified")
    submit = SubmitField('Submit')
@app.route('/delete-recipe', methods=['GET','POST'])
def delRecipe():
    form = DeleteForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('delete.html', form = form)
    
## Creates the form to add a new recipe
@app.route('/add-recipe', methods=['GET', 'POST'])
def update():
    
    form = InfoForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        ingredients = form.ingredients.data
        form.ingredients.data = ''
        instructions = form.instructions.data
        form.instructions.data = ''
        servingSize = form.servingSize.data
        form.servingSize.data = ''
        category = form.category.data
        form.category.data = ''
        notes = form.notes.data
        form.notes.data = ''
        dateAdded = form.dateAdded.data
        form.dateAdded.data = ''
        dateModified = form.dateAdded.data
        form.dateAdded.data = ''
    return render_template('add.html', form = form)
@app.route('/', methods=['GET'])
def test():
    return render_template('layout.html')
    
## returns all current recipes
@app.route('/recipes', methods=['GET'])
def returnAllRecipes():
    return jsonify({'recipes': recipes})

@app.route('/add-recipe')
def addRecipeHTML():
    return render_template('add.html')

@app.route('/delete-recipe')
def deleteRecipeHTML():
    return render_template('delete.html')

## Dynamic routing example
@app.route('/recipes/<name>')
def recipe(name):
    return "<h1>This is a page for {}</h1>".format(name)

## returns a recipe
@app.route('/recipes/<string:recipe>', methods=['GET'])
def returnOneRecipe(recipe):
    rec = [recip for recip in recipes if recip['name']==recipe]
    return jsonify({'recipe': rec[0]})

## adds a new recipe name
@app.route('/recipes', methods=['POST'])
def addRecipe():
    recipe = {
    'name': request.get_json(force=True).get('name')
    }

    recipes.append(recipe)
    return jsonify({'name': recipes})

## edit the name of a recipe
@app.route('/recipes/<string:recipe>', methods = ['PUT'])
def editRecipe(recipe):
    rec = [recip for recip in recipes if recip['name']==recipe]
    rec[0]['name'] = request.get_json(force=True).get('name')
    return jsonify({'recipe': rec[0]})

## Delete a recipe
@app.route('/recipes/<string:recipe>', methods = ['DELETE'])
def removeRecipe(recipe):
    rec = [recip for recip in recipes if recip['name']==recipe]
    recipes.remove(rec[0])
    return render_template('delete.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5003)