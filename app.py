import os
import requests
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

UPSTREAM_URL = "https://augestel.com/api/v1/iprn/messages"
TIMEOUT_SECONDS = int(os.environ.get("UPSTREAM_TIMEOUT", "30"))

# Only the parameters supported by the Augestel endpoint are forwarded.
ALLOWED_PARAMS = {
    "start_date",
    "end_date",
    "type",
    "per_page",
    "page",
}


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "service": "Augestel API endpoint",
        "endpoint": "/api/sms",
        "usage": "/api/sms?token=YOUR_AUGESTEL_API_KEY&start_date=YYYY-MM-DD"
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/sms")
def sms():
    # The supplied token is used as the Augestel Bearer API key.
    api_key = request.args.get("token", "").strip()
    if not api_key:
        return jsonify({
            "error": "Missing token",
            "message": "Pass your Augestel API key using the token query parameter."
        }), 400

    params = {
        key: request.args.get(key)
        for key in ALLOWED_PARAMS
        if request.args.get(key) is not None
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

    try:
        upstream = requests.get(
            UPSTREAM_URL,
            headers=headers,
            params=params,
            timeout=TIMEOUT_SECONDS,
        )

        # Return the upstream response body and HTTP status without reshaping JSON.
        response_headers = {}
        for name in ("Content-Type", "Retry-After"):
            if name in upstream.headers:
                response_headers[name] = upstream.headers[name]

        return Response(
            upstream.content,
            status=upstream.status_code,
            headers=response_headers,
        )

    except requests.Timeout:
        return jsonify({
            "error": "Upstream timeout",
            "message": "Augestel did not respond within the configured timeout."
        }), 504
    except requests.RequestException:
        return jsonify({
            "error": "Upstream connection failed",
            "message": "Could not connect to Augestel API."
        }), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "10000"))
    )
