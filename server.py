import os

from bottle import Bottle, request, static_file, route, get, template
from pathlib import Path
from hashlib import sha256


myhash = "407a7714ed0e531d4d4e2a3adc8f882630aa9ce059de02e1a1f8351f09c1bd31"

page_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>Password Validation</title>
    <link rel="stylesheet" href="https://itu-itis-2019.github.io/assignment1-ituitis-asan18/CSS/contact.css">
  </head>
  <body>
    %(body_text)s
    <table>
      <tr>
         <th style="border-bottom: dotted;">IP Adresses</th>
         <th style="border-bottom: dotted;">Count</th>
      </tr>
      %(table_content)s
    </table>
    <br></br>
    <a href= "/">Go to Home Page</a>
  </body>
</html>
"""

def create_hash(password):
    pw_bytestring = password.encode()
    return sha256(pw_bytestring).hexdigest()

my_dir = os.getcwd()

@route('/static/<filepath:path>')
def static_content(filepath):
    my_root = os.path.join(my_dir, 'static')
    return static_file(filepath, root=my_root)

ip_adresses = []
def home_page():
    header = request.environ
    global ip_adresses
    new_ip = new_ip = request.headers.get("X-Forward-For", "127.0.0.1")

    for ip in ip_adresses:
        if new_ip == ip["ip"]:
            ip["count"] += 1
            break
    else:
        ip_adresses.append({"ip": new_ip, "count": 1})

    visitors = {"ip_adresses": ip_adresses, "header": header}
    return template("index.html", visitors)

def password_check():
    password = request.forms.get('password')
    table_content = """ """
    if create_hash(password) == myhash and request.forms.get('show'):
        content = """
        <p>Password is correct.</p>
        <p>First Ip was: %(first_visitor)s</p>
        """
        content = content % {"first_visitor": ip_adresses[0]}
        ip_adresses.clear()
    elif create_hash(password) == myhash and request.forms.get('dontshow'):
        content = """
        <p>Password is correct.</p>
        """
        ip_adresses.clear()
    else:
        content = """
        <p>Sorry darling. You are not allowed.</p>
        """

    for ip in ip_adresses:
        table_content += """
        <tr>
            <td>%(ip)s</td>
            <td>%(count)s</td>
        </tr>
        """
        table_content = table_content % {"ip": ip["ip"], "count": ip["count"]}

    return page_template % {"body_text": content, "table_content": table_content}


def about_page():
    return template("about.html")

def projects_page():
    return template("projects.html")

def contact_page():
    return template("contact.html")

def create_app():
    app = Bottle()
    app.route("/static/<filepath:path>","GET",static_content)
    app.route("/", "GET", home_page)
    app.route("/contact.html", "GET", contact_page)
    app.route("/about.html", "GET", about_page)
    app.route("/projects.html", "GET", projects_page)
    app.route("/validation", "POST", password_check)
    return app


application = create_app()
application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
