from __future__ import annotations

from typing import Any, Dict, Optional

from flask import Flask, jsonify, request, send_from_directory

from password_generator import SYMBOLS, assess_strength, generate_password

app = Flask(__name__, static_folder=".", static_url_path="")

MIN_LENGTH = 4
MAX_LENGTH = 64


def _coerce_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(value, maximum))


@app.route("/")
def root() -> Any:  # pragma: no cover - simple file serving
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/generate")
def api_generate() -> Any:
    data: Optional[Dict[str, Any]] = request.get_json(silent=True) or {}
    length_raw = data.get("length", 14)
    use_symbols = bool(data.get("symbols", True))

    length = _clamp(_coerce_int(length_raw, 14), MIN_LENGTH, MAX_LENGTH)

    try:
        password = generate_password(length, use_symbols)
    except ValueError as exc:  # length guard
        return jsonify({"error": str(exc)}), 400

    strength, tips = assess_strength(password, use_symbols)
    return jsonify(
        {
            "password": password,
            "strength": strength,
            "tips": tips,
            "symbols": use_symbols,
            "length": length,
            "symbol_set": SYMBOLS,
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
