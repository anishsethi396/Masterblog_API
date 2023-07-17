from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_posts(data):
    """
    Validates the data dictionary for a post.
    :param data: A dictionary containing a post data.
    :return: True if "title" and "content" is present, False otherwise.
    """
    if "title" not in data or "content" not in data:
        return False
    return True


def find_post_by_id(post_id):
    """
    Find a post in the list of posts by its ID
    :param post_id: The ID of the post to find.
    :return: The post dictionary if found, None otherwise.
    """
    for post in POSTS:
        if post_id == post['id']:
            return post


def sort_post(sort, direction):
    """
    Sort the list of posts based on a given sort field and direction.
    """
    if direction == "asc":
        is_ascending = True
    elif direction == "desc":
        is_ascending = False
    else:
        is_ascending = True
    if sort is not None:
        sorted_post = sorted(POSTS, key=lambda x: x[sort].lower(), reverse=not is_ascending)
    else:
        sorted_post = sorted(POSTS, key=lambda x: x['id'], reverse=not is_ascending)
    return sorted_post


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieves and returns a sorted list of posts based on the provided query parameters.
    """
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    sorted_list = sort_post(sort, direction)
    return jsonify(sorted_list)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    """
    Add a new post to the list of posts.
    """
    new_post = request.get_json()
    if not validate_posts(new_post):
        return jsonify({"error": "Invalid post data"}), 400

    new_id = max(post['id'] for post in POSTS) + 1
    new_post['id'] = new_id

    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_posts(id):
    """
    Delete a post with the given ID from the list of posts.
    """
    post = find_post_by_id(id)
    if post is None:
        return ({"error": "Not Found"}), 404
    else:
        for individual_post in POSTS:
            if individual_post == post:
                POSTS.remove(individual_post)
                break
    return {"message": f"Post with id {id} has been deleted successfully."}


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    Updates a post with the given ID in the list of posts.
    """
    post = find_post_by_id(id)
    if post is None:
        return ({"error": "Not Found"}), 404
    new_data = request.get_json()
    if new_data is None:
        return jsonify(post)
    else:
        post.update(new_data)
        return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for posts based on the provided title and content query parameters.
    """
    title = request.args.get('title')
    content = request.args.get('content')
    post_list = []
    for post in POSTS:
        search_title = post.get("title")
        search_content = post.get("content")
        if title.lower() in search_title.lower() or content.lower() in search_content.lower():
            post_list.append(post)
    return jsonify(post_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
