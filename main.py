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
    try: 
      session['distance'] = request.args['distance']
    except: 
      assert 'distance' in session

    return get_restaurants(location=session['location'], category=session['category'], radius=session['distance'], price=session['price'])
  except:
    return "<script>window.location.href='start.html';</script>"


# generate restaurants list from api
@app.route('/test', methods=['GET'])
def get_restaurants(location="32816", category="asian", radius="15", price="4"):
  # build html
  
  # create request url
  api_url = "http://whatsnext.hsauers.net/find?"
  api_url += "location=" + location + "&category=" + category + "&radius=" + radius + "&money=" + price

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
  id_list = []

  restaurants_html = ""

  for r in restaurants:
    # generate restaurant html from template
    temp_html = ""
    with open('restaurant_template.html', 'r') as content_file:
      temp_html = content_file.read()
    
    # replace strings with data
    temp_html = temp_html.replace("NAME_ADDRESS", str(r['name'] + " - " + r['address']))
    temp_html = temp_html.replace("IMG_URL", str(r['image']))
    temp_html = temp_html.replace("NAME_DISTANCE", str(r['name'] + " - " + r['distance']))
    temp_html = temp_html.replace("REVIEW", str(r['review']))

    # @TODO: Return Business ID from Yelp API
    temp_html = temp_html.replace("REST_NAME", r['name'])
    temp_html = temp_html.replace("LOCATION", r['address'])

    temp_html = temp_html.replace("PHONE_NUMBER", r['phone'])
    temp_html = temp_html.replace("BIZ_ID", r['id'])
    id_list.append(r['id'])

    # append to all
    restaurants_html += temp_html

  # reads html templates
  top_html = ""
  with open('end_top.html', 'r') as content_file:
    top_html = content_file.read()

  bottom_html = ""
  with open('end_bottom.html', 'r') as content_file:
    bottom_html = content_file.read()

  # log data
  try:
    with open('history.csv', 'a+') as historyfile:
      if 'idtoken' in session:
        # time, email, name, location, category, price, distance, restaurant_idlist
        historyfile.write(str(time.time()) + ", " + session['email'] + ", " + session['name'] + ", " + location + ", " + category + ", " + price + ", " + radius + ", " + str(id_list) + "\n")
      else:
        historyfile.write(str(int(time.time())) + ", " + "IP: " + str(request.remote_addr) + ", " + "guest" + ", " + location + ", " + category + ", " + price + ", " + radius + ", " + str(id_list) + "\n")
  except:
    pass

  return top_html + restaurants_html + bottom_html
  

@app.route('/oauth', methods=['POST', 'GET'])
def oauth():
  try:
    session['email'] = request.form.get('email')
    session['idtoken'] = request.form.get('idtoken')
    session['name'] = request.form.get('name')
    return "Signed in as " + session['name']
  except:
    return "Bad request."


@app.route('/history.csv', methods=['GET'])
def show_history():
  return "404 not found"

  
# start listening
if __name__ == "__main__":
  app.run(debug=False, port='5000', host='0.0.0.0')
