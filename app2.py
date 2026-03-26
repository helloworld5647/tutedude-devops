from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://flaskuser:StrongPassword123@cluster0.feqrdcf.mongodb.net/mydb")
db = client["mydb"]
collection = db["todoitems"]


@app.route('/todo')
def todo_page():
    return render_template("todo.html")


@app.route('/submittodoitem', methods=['POST'])
def submit_todo():

    itemName = request.form.get("itemName")
    itemDescription = request.form.get("itemDescription")

    collection.insert_one({
        "itemName": itemName,
        "itemDescription": itemDescription
    })

    return "Todo Stored Successfully"



if __name__ == "__main__":
    app.run(debug=True)
