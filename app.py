from flask import Flask, render_template, request, redirect
from flask_pymongo import pymongo

CONNECTION_STRING= 'mongodb+srv://User:123@cluster0.t2fkn.mongodb.net/?retryWrites=true&w=majority'

client = pymongo.MongoClient(CONNECTION_STRING)

db = client.get_database('blog')
article_collection = pymongo.collection.Collection(db, 'articles')


app = Flask(__name__)

@app.route('/')
def index():
    articles = []
    for article in db.articles.find():
        articles.append(article)
    return render_template("index.html", articles = articles)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method=='POST':
        _id = int(request.form['_id'])
        title = request.form['title']
        date = request.form['date']
        text = request.form['text']
        article_collection.insert_one(
            {
             "_id": _id,
             "title": title,
             "date": date,
             "text": text
            })
        return redirect('/') 
    else:  
        return render_template("create.html") 

@app.route('/<_id>/update/', methods=('GET', 'POST'))
def update(_id):
    article = db.articles.find_one({"_id": int(_id)})
    if request.method=='POST':
        _id = int(request.form['_id'])
        title = request.form['title']
        date = request.form['date']
        text = request.form['text']
        article_collection.update_one({"_id": _id},
            {'$set': {
             "_id": _id,
             "title": title,
             "date": date,
             "text": text
            }})
        return redirect('/') 
    else:  
        return render_template("update.html", article = article) 

@app.route("/<_id>/delete/", methods=('GET', 'POST'))  
def delete (_id):  
    article_collection.delete_one({"_id": int(_id)})
    return redirect('/')  


if __name__ == "__main__":
    app.run(debug=True)
