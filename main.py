from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import requests
import json
import time


app = Flask(__name__, static_folder='.', static_url_path='', template_folder='')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET'])
def home():
  return render_template('/start.html')


@app.route('/categories', methods=['GET'])
def categories():
  session['location'] = request.args['location'] 
  print(session['location'])
  return redirect('/categories.html', code=200)


@app.route('/prices', methods=['GET'])
def prices():
  session['category'] = request.args['category']
  return redirect('/prices.html', code=200)


@app.route('/radius', methods=['GET'])
def radius():
  session['price'] = request.args['price']
  return redirect('/distance.html', code=200)


@app.route('/restaurants', methods=['GET'])
def restaurants():
  try: 
    session['distance'] = request.args['distance']
    return get_restaurants(location=session['location'], category=session['category'], radius=session['distance'], price=session['price'])
  except:
    return "<script>window.location.href='start.html';</script>"


# generate restaurants list from api
@app.route('/test', methods=['GET'])
def get_restaurants(location="32816", category="asian", radius="15", price="4", isOpen=False):
  # build html
  
  # create request url
  api_url = "http://ec2-18-191-161-179.us-east-2.compute.amazonaws.com/find?"
  api_url += "location=" + location + "&category=" + category + "&radius=" + radius + "&money=" + price

  if not isOpen:
    api_url += "&open=false"

  print(api_url)

  resp = requests.get(api_url).content

  # ensures slow responses don't break the app
  count = 0
  while count < 30:
    try:
      restaurants = json.loads(resp)
      break
    except:
      time.sleep(0.25)
      count += 1
  if count >= 30:
    return render_template('none.html')

  r = restaurants[0]

  restaurants_html = ""

  for r in restaurants:
    restaurants_html += '<p><a href="https://maps.google.com/maps?q=' + r['name'] + " - " + r['address'] + '"><img src="' + r['image'] + '"/> </a> <p> <h1>' + r['name'] + " - " + r['distance'] + "</h1><p> <h3> " + r['review'] + " </h3>"

  # restaurants_html = "<h1>" + str(r['name']) + "</h1>"
  # {"address":"504 N Alafaya Trl Ste 119","distance":"3.4 mi.","image":"https://s3-media2.fl.yelpcdn.com/bphoto/irQ-lMGggMcjqVymw8v1bA/o.jpg","name":"Top Top Hot Pot","phone":"(407) 901-8888","price":"$$","rating":4.0,"review":"\"Double double toil and TROUBLE, ate so much my belt just BUCKLED!  lol\n\nOne of my many birthday dinners over the weekend.\""}


  # reads html templates
  top_html = ""
  with open('end_top.html', 'r') as content_file:
    top_html = content_file.read()

  bottom_html = ""
  with open('end_bottom.html', 'r') as content_file:
    bottom_html = content_file.read()

  return top_html + restaurants_html + bottom_html
  
  
# start listening
if __name__ == "__main__":
  app.run(debug=False, port='5000', host='0.0.0.0')
