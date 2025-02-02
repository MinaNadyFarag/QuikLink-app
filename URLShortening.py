
    
from flask import Flask, request, render_template, redirect, jsonify   
import json
import os
from datetime import datetime
import random
import string
import requests

json_file = "repository.json"

        
if not os.path.exists(json_file):
    try:
        with open(json_file, 'w') as file:
            json.dump([], file)
    
    except Exception as e:
        print(f"Error {e}: While creating file.")
        
        
def get_urls():
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data        

def generate_short_url(length = 6):
    
    short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return short_url

def search_short_url(short_url):
    try:
        data = get_urls()
        for url in data:
            if url['Short_url'] == short_url:
                return url['Origin_url']
        
        return None
    
    except Exception as e:
        return jsonify({"Error {e}": "While reloading data from Json file!"}), 500

def saveinfile(data):
    try:
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
            return 200
        return 500
    except Exception as e:
        return {"error": str(e)}

def check_original_url(origin_url):
    data = get_urls()
    for url in data:
        if url['Origin_url'] == origin_url:
            return True
    return False

def getShortByOrigin(origin_url):
    data = get_urls()
    
    for url in data:
        if url['Origin_url'] == origin_url:
            return url['Short_url']
    return None
 
app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route('/quicklink', methods=['POST'])
def get_URL():
    url = request.get_json()
    
    if 'url' not in url:
        return jsonify({"Error 400 (Bad Request)": "URL is needed!"}), 400
    
    origin_url = url['url']
    
    try:
        if check_original_url(origin_url):
            short_url = getShortByOrigin(origin_url)
            
            return jsonify({"Short_url" : short_url}), 201
    except Exception as e:
        print("it's new url")
    
    if not origin_url.startswith(('http://', 'https://')):
        origin_url = 'http://'+origin_url
    
    try:
        response = requests.get(origin_url)
        if response.ok:
            
            short_url = generate_short_url()
            
            with open(json_file, 'r') as file:
                data = json.load(file)
            
            current_dateTime = datetime.now()
            
            newUrl = {
                'ID': len(data),
                'Short_url': short_url,
                'Origin_url': origin_url,
                'Date': current_dateTime.strftime('%d-%m-%Y'),
                'Time': current_dateTime.strftime('%H:%M:%S')
            }
            
            data.append(newUrl)
            
            saveinfile(data)

            return jsonify({"Short_url": short_url}), 201
            
        else:
            return jsonify({"Error 400 (Bad Request): URL is not valid or not reachable!"})
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 400
    

    
@app.route('/quicklink/<short_url>', methods=['GET'])
def redirect_short_url(short_url):
    origin_url = search_short_url(short_url)
    
    if origin_url == None:
        return jsonify({"Error 404 (Not Found)": "There is no such a short URL!"}), 404
    
    return redirect(origin_url, code=301)
    
@app.route('/quicklink/<short_url>', methods=['PUT'])
def alter_origin_url(short_url):
    new_request = request.get_json()
    
    if not 'url' in new_request:
        return jsonify({"ERROR 400 (Bad Request): Enter new URL to alter"}), 400

    url = new_request['url']
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    response = requests.get(url)
    
    if response.ok:
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
            
            for item in data:
                if item['Short_url'] == short_url:
                    item['Origin_url'] = url
                    
                    saveinfile(data)
                        
                    return jsonify({"State":"URL has been altered successfully:)"}), 200
                
            return jsonify({"ERROR 400 (Bad Request)":short_url + " is not found!"})
        
        except Exception as e:
            return jsonify({f"ERROR {e}": "While reading json file!"})
        
@app.route('/quicklink/<short_url>', methods=['DELETE'])
def delete_url(short_url):
    try:
        with open(json_file, 'r') as file:
            savedULRs = json.load(file)
            
        for url in savedULRs:
            if url['Short_url'] == short_url:
                savedULRs.remove(url)
                saveinfile(savedULRs)
                return jsonify({f"URL {short_url}": "Has been deleted successfully:)"})
        return jsonify({"ERROR": "There is no such URL <" +short_url+">"}), 404
    
    except Exception as e:
        return jsonify({f"ERROR": f"While deleting URL <{short_url}>: {e}"}), 500
    
@app.route('/')
def api_ui():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)
    
# الكود دا ناقصه انه يتاكد ان الباث اللي مبعوت له جديد و لو متكرر يرجع نفس الشورت  (بقي بيعمل كدا لكن لازم الباث يبدا ب اتش تي تي بي علي الاقل او اس) و كمان يرتب الباثات المحفوظة 