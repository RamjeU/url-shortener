import random
import string
from urllib.parse import urlparse

from flask import Blueprint, jsonify, request, redirect

from app.database import insert_url, get_url, code_exists, increment_clicks

bp = Blueprint("routes", __name__)

CODE_LENGTH = 6
CODE_CHARS = string.ascii_letters + string.digits


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False


def generate_short_code():
    while True:
        code = "".join(random.choices(CODE_CHARS, k=CODE_LENGTH))
        if not code_exists(code):
            return code


@bp.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json(silent=True)
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' field in request body"}), 400

    original_url = data["url"].strip()
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL. Must include http:// or https://"}), 400

    custom_code = data.get("custom_code")
    if custom_code:
        if code_exists(custom_code):
            return jsonify({"error": "Custom code already in use"}), 409
        short_code = custom_code
    else:
        short_code = generate_short_code()

    insert_url(short_code, original_url)

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code,
        "original_url": original_url,
    }), 201


@bp.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code):
    row = get_url(short_code)
    if row is None:
        return jsonify({"error": "Short code not found"}), 404

    increment_clicks(short_code)
    return redirect(row["original_url"])


@bp.route("/api/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    row = get_url(short_code)
    if row is None:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "short_code": row["short_code"],
        "original_url": row["original_url"],
        "clicks": row["clicks"],
        "created_at": row["created_at"],
    })
