import os
from flask import Flask, jsonify, request, render_template, url_for, session, redirect
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_required
from flask_jwt import JWT
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,DateTimeField,TextField
from wtforms.validators import DataRequired



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
api = Api(app)
app.secret_key = 'jason'
login = LoginManager(app)
app.config['SECRET_KEY']== 'jason'





recipes = []
class RecipeNames(Resource):
    def get(self, name):
        for recipe in recipes:
            if recipe['name'] ==name:
                return recipe
        return {'name': None}

    def post(self, name):
        recipe = {'name': name}
        recipes.append(recipe)
        return recipe

    def delete(self,name):
        for ind,pup in enumerate(recipes):
            if pup['name']==name:
                deleted_recipe = recipes.pop(ind)
                return {'note': 'delete success'}

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

@app.route('/delete-recipe', methods=['GET','POST'])
def delRecipe():
    form = DeleteForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('delThanks'))        
    return render_template('delete.html', form = form)

@app.route('/del-recipe/thanks')
def delThanks():
    return render_template('deleteThanks.html')


@app.route('/delete-recipe')
def deleteRecipeHTML():
    return render_template('delete.html')


@app.route('/edit-recipe', methods = ['GET', 'POST'])
def editRecipe():
    form = EditForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['ingredients'] = form.ingredients.data
        session['instructions'] = form.instructions.data
        session['servingSize'] = form.servingSize.data
        session['category'] = form.category.data
        session['notes'] = form.notes.data
        session['dateAdded'] = form.dateAdded.data
        session['dateModified'] = form.dateAdded.data
        return redirect(url_for('editThanks'))
    return render_template('edit.html', form = form)

@app.route('/edit-recipe/thanks')
def editThanks():
    return render_template('editThanks.html')

@app.route('/edit-recipe')
def editRecipeHTML():
    return render_template('edit.html')




## Creates the form to add a new recipe
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
        session['dateModified'] = form.dateAdded.data

        return redirect(url_for('addThanks'))
    return render_template('add.html', form = form)

@app.route('/add-recipe')
def addRecipeHTML():
    return render_template('add.html')

@app.route('/add-recipe/thanks')
def addThanks():
    return render_template('addThanks.html')


@app.route('/', methods=['GET'])
def test():
    return render_template('layout.html')
    
## returns all current recipes
@app.route('/recipes', methods=['GET'])
def returnAllRecipes():
    return jsonify({'recipes': recipes})






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