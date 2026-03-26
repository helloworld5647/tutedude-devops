from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb+srv://flaskuser:StrongPassword123@cluster0.feqrdcf.mongodb.net/mydb?retryWrites=true&w=majority")

db = client.todo_db
collection = db.items

@app.route('/submittodoitem', methods=['POST'])
def submit_todo():

    itemName = request.form.get('itemName')
    itemDescription = request.form.get('itemDescription')

    collection.insert_one({
        "itemName": itemName,
        "itemDescription": itemDescription
    })

    return "Todo Item Stored Successfully"
