import os

from bottle import Bottle, request, static_file, route, get, template
from pathlib import Path

my_dir = os.getcwd()

@route('/static/<filepath:path>')
def static_content(filepath):
    my_root = os.path.join(my_dir, 'static')
    return static_file(filepath, root=my_root)

ip_adresses = []
def home_page():
    global ip_adresses
    new_ip = request.headers.get("X Forwarded-For", "127.0.0.1")

    for ip in ip_adresses:
        if new_ip == ip["ip"]:
            ip["count"] += 1
            break
    else:
        ip_adresses.append({"ip": new_ip, "count": 1})

    return Path("index.html").read_text()

def about_page():
    return template("about.html")

def projects_page():
    return template("projects.html")

def contact_page():
    ip_info = {"ip_adresses": ip_adresses}
    return template("contact.html", ip_info)

def create_app():
    app = Bottle()
    app.route("/static/<filepath:path>","GET",static_content)
    app.route("/index.html", "GET", home_page)
    app.route("/contact.html", "GET", contact_page)
    app.route("/about.html", "GET", about_page)
    app.route("/projects.html", "GET", projects_page)
    return app


application = create_app()
application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
