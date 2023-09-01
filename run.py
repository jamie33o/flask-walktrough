import os
from flask import Flask, render_template,request,flash
import json
if os.path.exists("env.py"):
    import env

#create instance of imported flask and store in variable app
#__name__(the first argument) is the name of the application module or package we can use __name__ which is built in python variable
#because we are only using one module flask needs this to know where to look for templates and static files
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


# @ is decourater its a way of wrapping a function when we try to browse to the
# route directory as indicated by the "/" then flask trigers the index function
@app.route("/")
def index():
    return render_template("index.html")


# routing bind to a view
# this function is called route or view 
# when we go to the "/" on the top level of our domain it then returns the template from the index function
# the route decorator binds the index function to its self so that when that route is called then that function is called
@app.route("/about")
def about():
    data =[]
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("about.html", page_title="About", company=data)


@app.route("/about/<member_name>")
def about_member(member_name):
    member = {}
    with open("data/company.json" , "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == member_name:
                member = obj
    return  render_template("member.html", member=member)

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))
        print(request.form.get("name"))
        print(request.form["email"])
    return render_template("contact.html", page_title="Contact")

@app.route("/careers")
def careers():
    return render_template("careers.html", page_title="Careers")


if __name__ == "__main__":
    
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True
    )
