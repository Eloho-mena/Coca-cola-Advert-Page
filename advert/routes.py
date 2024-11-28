from flask import request, jsonify,render_template
from models import db, Comment, Advert
from app import app

@app.route('/')
def home():
    return render_template('index.html') 
@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.json
    new_comment = Comment(content=data['content'], advert_id=data['advert_id'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment created", "comment": new_comment.content}), 201

@app.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify([{"id": c.id, "content": c.content, "likes": c.like_count, "dislikes": c.dislike_count, "replies": [{"id": r.id, "content": r.content} for r in c.replies]} for c in comments])

@app.route('/comments/<int:id>/like', methods=['POST'])
def like_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.like_count += 1
    db.session.commit()
    return jsonify({"message": "Like added", "likes": comment.like_count})

@app.route('/comments/<int:id>/dislike', methods=['POST'])
def dislike_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.dislike_count += 1
    db.session.commit()
    return jsonify({"message": "Dislike added", "dislikes": comment.dislike_count})

@app.route('/comments/<int:id>/reply', methods=['POST'])
def reply_comment(id):
    parent_comment = Comment.query.get_or_404(id)
    data = request.json
    reply = Comment(content=data['content'], advert_id=parent_comment.advert_id, parent_id=parent_comment.id)
    db.session.add(reply)
    db.session.commit()
    return jsonify({"message": "Reply added", "reply": reply.content})

@app.route('/advert/likes-dislikes', methods=['GET'])
def get_advert_likes_dislikes():
    advert = Advert.query.first()
    return jsonify({"likes": advert.like_count, "dislikes": advert.dislike_count})

@app.route('/advert/like', methods=['POST'])
def like_advert():
    advert = Advert.query.first()
    advert.like_count += 1
    db.session.commit()
    return jsonify({"message": "Advert liked", "likes": advert.like_count})

@app.route('/advert/dislike', methods=['POST'])
def dislike_advert():
    advert = Advert.query.first()
    advert.dislike_count += 1
    db.session.commit()
    return jsonify({"message": "Advert disliked", "dislikes": advert.dislike_count})
