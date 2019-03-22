import os
from flask import Flask, jsonify, request, render_template, url_for, session, redirect
from flask_restful import Resource, Api
from flask_jwt import JWT
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,DateTimeField,TextField
from wtforms.validators import DataRequired


app = Flask(__name__)
api = Api(app)
app.secret_key = 'jason'
login = LoginManager(app)
app.config['SECRET_KEY']== 'jason'
recipes = []
fields = ['Name', 'Ingredients', 'Instructions', 'Serving Size', 'Category', 'Notes', 'Date Added', 'Date Modified']

class DeleteForm(FlaskForm):
    name = StringField("What recipe would you like to delete?")
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    name = StringField("What is the name of the recipe?")
    ingredients = StringField("What are the ingredients involved?")
    instructions = StringField("What are the instructions to make this recipe?")
    servingSize = StringField("What is the serving size?")
    category = StringField("What type of food is this?")
    notes = StringField("Enter any notes here")
    dateAdded = StringField("Date added")
    dateModified = StringField("Date modified")
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
    recipe = []

@app.route('/', methods=['GET'])
def test():
    return render_template('layout.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/list-recipes', methods = ['GET'])
def listRecipesHTML():
    form = InfoForm
    return render_template('listRecipes.html', recipes = recipes, fields = fields)

@app.route('/add-recipe')
def addRecipeHTML():
    return render_template('add.html')

@app.route('/add-recipe', methods=['GET', 'POST'])
def update():
    recipe = []
    form = InfoForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['ingredients'] = form.ingredients.data
        session['instructions'] = form.instructions.data
        session['servingSize'] = form.servingSize.data
        session['category'] = form.category.data
        session['notes'] = form.notes.data
        session['dateAdded'] = form.dateAdded.data
        session['dateModified'] = form.dateModified.data
        recipe.append(form.name.data)
        recipe.append(form.ingredients.data)
        recipe.append(form.instructions.data)
        recipe.append(form.servingSize.data)
        recipe.append(form.category.data)
        recipe.append(form.notes.data)
        recipe.append(form.dateAdded.data)
        recipe.append(form.dateModified.data)
        recipes.append(recipe)
        return redirect(url_for('addThanks'))
    return render_template('add.html', form = form)

@app.route('/add-recipe/thanks')
def addThanks():
    return render_template('addThanks.html')

@app.route('/edit-recipe')
def editRecipeHTML():
    return render_template('edit.html', recipes = recipes)

@app.route('/edit-recipe', methods = ['GET', 'POST'])
def editRecipe():
    form = EditForm()
    recipe = []
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['ingredients'] = form.ingredients.data
        session['instructions'] = form.instructions.data
        session['servingSize'] = form.servingSize.data
        session['category'] = form.category.data
        session['notes'] = form.notes.data
        session['dateAdded'] = form.dateAdded.data
        session['dateModified'] = form.dateModified.data
        recipe.append(form.name.data)
        recipe.append(form.ingredients.data)
        recipe.append(form.instructions.data)
        recipe.append(form.servingSize.data)
        recipe.append(form.category.data)
        recipe.append(form.notes.data)
        recipe.append(form.dateAdded.data)
        recipe.append(form.dateModified.data)
        recipes.append(recipe)
        for i in recipes:
            if form.name.data == i[0]:
                recipes.remove(i)
                break
        return redirect(url_for('editThanks'))
    return render_template('edit.html', form = form, recipes = recipes)

@app.route('/edit-recipe/thanks')
def editThanks():
    return render_template('editThanks.html', recipes = recipes)

@app.route('/delete-recipe')
def deleteRecipeHTML():
    return render_template('delete.html')

@app.route('/delete-recipe', methods=['GET','POST'])
def delRecipe():
    form = DeleteForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        for i in recipes:
            if form.name.data == i[0]:
                recipes.remove(i)
        return redirect(url_for('delThanks'))        
    return render_template('delete.html', form = form)

@app.route('/del-recipe/thanks')
def delThanks():
    return render_template('deleteThanks.html', recipes = recipes)

if __name__ == '__main__':
    app.run(debug=True, port=5003)