from flask import Flask, render_template, request
# just serve all the static files under root
app = Flask(__name__, static_folder='.', static_url_path='', template_folder='')

# hold user's data
category = ""
price = ""
distance = ""
location = ""

@app.route('/', methods=['GET'])
def home():
  return render_template('/start.html')


@app.route('/categories', methods=['GET'])
def categories():
  location = request.args['location']
  return render_template('/categories.html')


@app.route('/prices', methods=['GET'])
def prices():
  category = request.args['category']
  return render_template('/prices.html')


@app.route('/radius', methods=['GET'])
def radius():
  distance = request.args['distance']
  return render_template('distance.html')


@app.route('/restaurants', methods=['GET'])
def restaurants():
  price = request.args['price']
  return get_restaurants(location=location, category=category, radius=distance, price=price)


# generate restaurants list from api
def get_restaurants(location, category, radius, price):
  # build html
  return  """
          <html><body><h1>RESTAURANTS</h1></body></html>
          """
  
  
# start listening
if __name__ == "__main__":
    app.run(debug=True, port='8080', host='0.0.0.0')
