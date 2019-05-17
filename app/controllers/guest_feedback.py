from flask import Blueprint, render_template, request, jsonify
from app.models import Post, Like, db

guest_feedback = Blueprint(
    'guest_feedback',
    __name__
)

@guest_feedback.route('/like', methods=['POST'])
def like():
    like_forsql = Like()
    like_forsql.Like_Type = 1
    db.session.add(like_forsql)
    db.session.commit()
    like_count = Like.query.filter(Like.Like_Type == 1).count()
    cancellike = Like.query.filter(Like.Like_Type == 0).count()
    like_count = like_count - cancellike
    back_data = {'like_count': like_count}
    return jsonify(back_data)

@guest_feedback.route('/cancel_like', methods=['POST'])
def cancel_like():
    like_forsql = Like()
    like_forsql.Like_Type = 0
    db.session.add(like_forsql)
    db.session.commit()
    like_count = Like.query.filter(Like.Like_Type == 1).count()
    cancellike = Like.query.filter(Like.Like_Type == 0).count()
    like_count = like_count - cancellike
    back_data = {'like_count': like_count}
    return jsonify(back_data)