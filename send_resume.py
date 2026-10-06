import hashlib
import hmac
import json
import os

import requests
from dotenv import load_dotenv


def send_resume(endpoint, resume_url, secret, notes):
    """
    POST to HowGood's job application endpoint.

    Given POST details, send the payload to HowGood's endpoint and return
    the response details.
    """
    payload = {
        "name": "Melanie Arbor",
        "email": "m@melaniearbor.com",
        "resume": resume_url,
        "location": "San Diego, CA (Remote)",
        "linkedin": "https://www.linkedin.com/in/melaniearbor/",
        "codeLink": "https://github.com/melaniearbor/howgoodapplication",
        "yearsPython": 11,
        "yearsDjango": 10,
        "notes": notes,
    }

    body = json.dumps(payload)
    signature = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()

    response = requests.post(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json", "X-HMAC-Signature": signature},
        timeout=10,
    )
    response_payload = response.json()
    return response.status_code, response_payload


def main():
    """
    Execute send_resume with the correct details and data.
    """
    load_dotenv()

    secret = os.getenv("SECRET")
    endpoint = os.getenv("ENDPOINT")
    resume_url = os.getenv("RESUME_URL")
    notes = os.getenv("NOTES")
    if not all([secret, endpoint, resume_url]):
        print("SECRET, ENDPOINT, or RESUME_URL missing from .env / environment")
        return
    status, response = send_resume(
        endpoint=endpoint, resume_url=resume_url, secret=secret, notes=notes
    )
    print(status)
    print(response)


if __name__ == "__main__":  # pragma: no cover
    main()
