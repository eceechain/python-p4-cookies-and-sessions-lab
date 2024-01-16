#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False  # Use 'app.json_encoder' instead of 'app.json.compact'

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = []
    for article in Article.query.all():
        article_dict = {
            "id": article.id,
            "author": article.author,
            "title": article.title,
            "content": article.content,
            "preview": article.preview,
            "minutes_to_read": article.minutes_to_read,
            "date": article.date
        }
        articles.append(article_dict)

    response = make_response(
        jsonify(articles),
        200
    )

    return response

@app.route('/articles/<int:id>')
def show_article(id):
    # Set session['page_views'] to an initial value of 0 if it's the first request for this user
    session['page_views'] = session.get('page_views', 0)

    # Increment the value of session['page_views'] by 1 for every request
    session['page_views'] += 1

    # Check if the user has viewed 3 or fewer pages
    if session['page_views'] <= 3:
        article = Article.query.filter(Article.id == id).first()
        if article:
            article_dict = {
                "id": article.id,
                "author": article.author,
                "title": article.title,
                "content": article.content,
                "preview": article.preview,
                "minutes_to_read": article.minutes_to_read,
                "date": article.date
            }

            response = make_response(
                jsonify(article_dict),
                200
            )

            return response
        else:
            return {'message': '404: Article not found'}, 404
    else:
        # If the user has viewed more than 3 pages, return an unauthorized error message
        return {'message': 'Maximum pageview limit reached'}, 401

if __name__ == '__main__':
    app.run(port=5555)