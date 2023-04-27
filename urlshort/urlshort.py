from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename


bp = Blueprint('urlshort',__name__ ) #bp short name for blueprint and specifying the file name which have urlshort.py
            #A blueprint is a template for generating a "section" of a web application. You can think of it as a mold:
            #You can take the blueprint and apply it to your application in several places. 
            # Each time you apply it the blueprint will create a new version of its structure in the plaster of your application.
            #For bigger projects, all your code shouldn't be in the same file. 
            # Instead you can segment or split bigger codes into separate files, mostly based on functionality

@bp.route('/') # we mapping the route to specific url
def home(): #defining the home function
    return render_template('home.html', codes=session.keys()) 


@bp.route('/your-url', methods=['GET','POST'])
def your_url():  #python files doesnt allow to give - in functions
    if request.method == 'POST':
        urls = {}     # we are creating urls dictionary

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file: # we are checking for previously exist json and loading that file data into our new json file
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select Name')  # if the key(shortname) is same as the previous json file data it will return back to home page
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():  # checking the whether the user is adding file or url
            urls[request.form['code']]={'url':request.form['url']} #saving the url for particular code(shortname)
        else: # if it is file uploading file
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename) # giving filename with secure which doesn't harm with any delete or anything which is safe
            f.save('/Users/Srinidhi.mahanthe/Desktop/Url-shortener/urlshort/static/user_files/' + full_name) # saving the filewith path
            urls[request.form['code']]={'file':full_name}  #updating the json file with new information

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True #cookie where we store or see the url which we have created when we comeback again for temporary
        return render_template('your_url.html', code=request.form['code'])  # we used a variable called code to jinja so that we could display that back on the web browser
    else:
        return redirect(url_for('purlshort.home'))
    # GET means all the data will be displayed in the url 


@bp.route('/<string:code>') # loooks for the string inside the variable which is named as code (this route is for making shortname to take to the preffered url website)
def redirect_to_url(code): #same as line 43 look for a string after a / inputed in a variable called code
    if os.path.exists('urls.json'): #checkig if urls json is there or not
        with open('urls.json') as urls_file: 
            urls = json.load(urls_file) #loading the data into the file
            if code in urls.keys(): # finding the appropriate key we are looking for(it will tell the code entered matches anything here and display it back to the user)
                if 'url' in  urls[code].keys(): # this we are distinguish between url or file by specifying url
                    return redirect(urls[code]['url'])
                else: # creates a url for static files 
                    return redirect(url_for('static', filename = 'user_files/' + urls[code]['file']))
    return abort(404) # rather display different message flask method not found is better 


@bp.errorhandler(404) # rather than displaying method not found display our own error page thats error handling
def page_not_found(error):
    return render_template('page_not_found.html'), 404 


@bp.route('/api') # creating an api and showing the created codes(shortname) by any user inside the api using jsonify
def session_api():
    return jsonify(list(session.keys()))




