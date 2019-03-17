from flask import Flask, jsonify, request, render_template, url_for
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_required
from flask_jwt import JWT
from security import authenticate, identity
app = Flask(__name__)
app.secret_key = 'jason'
login = LoginManager(app)
jwt = JWT(app, authenticate, identity) # /auth

recipes = [{'name': 'lasagna', 'date added': '3/16/2019','ingredients': ['cheese', 'tomato sauce', 'ground beef'], 
'serving size': '2 people'},{'name': 'pizza'}]





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
    return jsonify({'recipe': recipes})

if __name__ == '__main__':
    app.run(debug=True, port=5003)