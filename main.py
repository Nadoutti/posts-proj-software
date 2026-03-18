import requests
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/posts"
mongo = PyMongo(app)

"""
   - Create a new post
"""


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json

    # verify if the user exists

    user = requests.get(f"http://users-app/users/{data['user_id']}")
    if user.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    result = mongo.db.posts.insert_one(data)  # type: ignore
    data["_id"] = str(result.inserted_id)

    return jsonify(data), 201


"""
   - Update an existing post
"""


@app.route("/posts/<uuid:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.json

    result = mongo.db.posts.update_one({"_id": post_id}, {"$set": data})  # type: ignore

    if result.matched_count == 0:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(data), 200


"""
    - Delete an existing post
"""


@app.route("/posts/<uuid:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = mongo.db.posts.find_one({"_id": post_id})  # type: ignore

    if post is None:
        return jsonify({"error": "Post not found"}), 404

    mongo.db.posts.delete_one({"_id": post_id})  # type: ignore

    return "", 204


"""
    - Get an existing post
"""


@app.route("/posts/<uuid:post_id>", methods=["GET"])
def get_post(post_id):
    post = mongo.db.posts.find_one({"_id": post_id})  # type: ignore

    if post is None:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(post), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
