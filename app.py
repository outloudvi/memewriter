import mwclient
from flask import Flask, request, redirect, url_for, jsonify
app = Flask(__name__)
site = mwclient.Site("meme.outv.im", "/")


@app.route('/', methods=['GET', 'POST'])
def do_login():
    if request.method == 'GET':
        return app.send_static_file("login.html")
    else:
        global site
        try:
            site.login(request.form["username"], request.form["password"])
        except mwclient.errors.LoginError as r:
            return str(r)
        return redirect(url_for('do_edit'))


@app.route('/editor', methods=['GET'])
def do_edit():
    return app.send_static_file("editor.html")


@app.route('/send', methods=['POST'])
def send_edit():
    global site
    data = request.get_json()
    page = site.pages[data["title"]]
    if page.exists:
        print(data["title"], ": This page already exists!")
    else:
        print(data["title"], ": No such page")
    page.save(data["content"], summary=data["summary"])
    print(data["title"], ": Saved")
    return "OK"


@app.route('/there', methods=['POST'])
def is_there():
    global site
    data = request.get_json()
    return jsonify({"exists": site.pages["JISFW:" + str(data["id"])].exists})
