from __future__ import annotations

from typing import Any, Dict, Optional

from flask import Flask, jsonify, request, send_from_directory

from password_generator import (
    SYMBOLS,
    assess_strength,
    estimate_entropy_and_crack_time,
    generate_password,
)

app = Flask(__name__, static_folder=".", static_url_path="")

MIN_LENGTH = 4
MAX_LENGTH = 64


def _coerce_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return value != 0
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
    use_symbols = _coerce_bool(data.get("symbols", True), True)
    use_upper = _coerce_bool(data.get("upper", True), True)
    use_lower = _coerce_bool(data.get("lower", True), True)
    use_digits = _coerce_bool(data.get("digits", True), True)

    length = _clamp(_coerce_int(length_raw, 14), MIN_LENGTH, MAX_LENGTH)

    try:
        password = generate_password(
            length,
            use_symbols=use_symbols,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
        )
    except ValueError as exc:  # length guard
        return jsonify({"error": str(exc)}), 400

    strength, tips = assess_strength(
        password,
        symbols_allowed=use_symbols,
        upper_allowed=use_upper,
        lower_allowed=use_lower,
        digits_allowed=use_digits,
    )

    entropy_bits, crack_seconds, crack_display = estimate_entropy_and_crack_time(
        length,
        use_upper=use_upper,
        use_lower=use_lower,
        use_digits=use_digits,
        use_symbols=use_symbols,
    )
    return jsonify(
        {
            "password": password,
            "strength": strength,
            "tips": tips,
            "symbols": use_symbols,
            "length": length,
            "symbol_set": SYMBOLS,
            "entropy_bits": entropy_bits,
            "crack_time_seconds": crack_seconds,
            "crack_time_display": crack_display,
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
