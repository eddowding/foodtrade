import json

ingredient_tree = '[[{"ingredientId":"54b6d44e0eaefa26f5c88ffd","dishId":"54b4e15d0eaefa5f038d177c","children":[[{"ingredientId":"54b8c8930eaefa04833c5d59","dishId":"54b4e15d0eaefa5f038d177c","children":[[]]},{"ingredientId":"54b8c89f0eaefa04833c5d5a","dishId":"54b4e15d0eaefa5f038d177c","children":[[]]},{"ingredientId":"54b8c8a60eaefa04833c5d5b","dishId":"54b4e15d0eaefa5f038d177c","children":[[]]},{"ingredientId":"54b8c8ae0eaefa04833c5d5c","dishId":"54b4e15d0eaefa5f038d177c","children":[[{"ingredientId":"54ba4a720eaefa44fd67a5df","dishId":"54b4e15d0eaefa5f038d177c","children":[[]]}]]},{"ingredientId":"54b8c8c60eaefa04833c5d5d","dishId":"54b4e15d0eaefa5f038d177c","children":[[]]}]]},{"ingredientId":"54ba4a790eaefa44fd67a5e0","dishId":"54b4e15d0eaefa5f038d177c","children":[[]]}]]'

def walk(ingredients, parent=None):
    for ingredient in ingredients:
        if isinstance(ingredient, list):
            walk(ingredient, parent)
        elif isinstance(ingredient, dict) and len(ingredient['children'][0]):
            print {'dishId': ingredient['dishId'], 'parentId': parent, 'ingredientId': ingredient['ingredientId']}
            walk(ingredient['children'], ingredient['ingredientId'])
        else:
            print {'dishId': ingredient['dishId'], 'parentId': parent, 'ingredientId': ingredient['ingredientId']}


if __name__ == '__main__':
    ingredients = json.loads(ingredient_tree)
    walk(ingredients)
