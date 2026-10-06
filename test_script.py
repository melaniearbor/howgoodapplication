import hashlib
import hmac
import json
import os

import pytest
import requests
import responses
from dotenv import load_dotenv

from script import main, send_resume

# override=True so the .env.tests values win even if the developer's
# shell already exports SECRET/ENDPOINT/RESUME_URL with active values
# (python-dotenv does not override existing variables by default).
load_dotenv(".env.tests", override=True)

resume_url = os.getenv("RESUME_URL")
secret = os.getenv("SECRET")
endpoint = os.getenv("ENDPOINT")


@pytest.fixture
def body():
    payload = {
        "name": "Melanie Arbor",
        "email": "m@melaniearbor.com",
        "resume": resume_url,
        "location": "San Diego, CA (Remote)",
        "linkedin": "https://www.linkedin.com/in/melaniearbor/",
        "codeLink": "https://github.com/melaniearbor/howgoodapplication",
        "yearsPython": 11,
        "yearsDjango": 10,
    }
    return json.dumps(payload)


@pytest.fixture
def signature(body):
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()


@responses.activate
def test_send_resume_url_results():
    """
    send_resume returns the correct data from the response.
    """
    responses.post(
        endpoint,
        status=400,
        json="Whoopsie",
    )
    code, message = send_resume(
        endpoint=endpoint,
        resume_url=resume_url,
        secret=secret,
    )

    assert code == 400
    assert message == "Whoopsie"


@responses.activate
def test_signature(signature):
    """
    The correct signature is provided in the header.
    """
    response = responses.post(
        endpoint,
        headers={"Content-Type": "application/json", "X-HMAC-Signature": signature},
        json={"message": "success"},
    )
    _, _ = send_resume(
        endpoint=endpoint,
        resume_url=resume_url,
        secret=secret,
    )
    assert response.calls[0].request.headers["X-HMAC-Signature"] == signature
    request_body = response.calls[0].request.body
    actual_signature = hmac.new(
        secret.encode(), request_body.encode(), hashlib.sha256
    ).hexdigest()
    assert actual_signature == signature


@pytest.fixture
def test_env(monkeypatch):
    """
    Pin the environment to the .env.tests values for main().

    load_dotenv inside script is stubbed out so main() never reads .env,
    and the three variables are set explicitly so main() cannot pick up
    any active values. monkeypatch undoes all of this after the test.
    """
    monkeypatch.setattr("script.load_dotenv", lambda *args, **kwargs: None)
    monkeypatch.setenv("SECRET", secret)
    monkeypatch.setenv("ENDPOINT", endpoint)
    monkeypatch.setenv("RESUME_URL", resume_url)


@responses.activate
def test_main_sends_to_test_endpoint(test_env):
    """
    main() sends exactly one request, and it goes to the .env.tests
    endpoint with the .env.tests resume URL.

    Only the test endpoint is registered, and responses raises
    ConnectionError for any unregistered URL — so if main() tried to
    use the active endpoint from .env, this test would fail rather
    than reach the real application.
    """
    response = responses.post(endpoint, status=201, json={"message": "received"})

    main()

    assert len(response.calls) == 1
    request = response.calls[0].request
    assert request.url == endpoint
    assert json.loads(request.body)["resume"] == resume_url


@responses.activate
def test_main_prints_status_and_response(test_env, capsys):
    """
    main() prints the status code and the response body.
    """
    responses.post(endpoint, status=201, json={"message": "received"})

    main()

    assert capsys.readouterr().out.splitlines() == [
        "201",
        "{'message': 'received'}",
    ]


@responses.activate
def test_bad_response_raises(test_env):
    """A response missing a JSON payload propagates from main()."""
    responses.post(endpoint, status=500)

    with pytest.raises(requests.exceptions.JSONDecodeError):
        main()


@responses.activate
def test_main_signature(test_env):
    """
    main() signs the request body with the .env.tests secret.
    """
    response = responses.post(endpoint, json={"message": "success"})

    main()

    request_body = response.calls[0].request.body
    expected_signature = hmac.new(
        secret.encode(), request_body.encode(), hashlib.sha256
    ).hexdigest()
    assert response.calls[0].request.headers["X-HMAC-Signature"] == expected_signature


@responses.activate
@pytest.mark.parametrize(
    ("variable", "value"),
    [
        pytest.param("SECRET", None, id="SECRET-missing"),
        pytest.param("ENDPOINT", None, id="ENDPOINT-missing"),
        pytest.param("RESUME_URL", None, id="RESUME_URL-missing"),
        pytest.param("SECRET", "", id="SECRET-empty"),
        pytest.param("ENDPOINT", "", id="ENDPOINT-empty"),
        pytest.param("RESUME_URL", "", id="RESUME_URL-empty"),
    ],
)
def test_missing_env_variable(test_env, monkeypatch, variable, value, capsys):
    """
    Missing or empty env variables fail loudly.

    If any of SECRET, ENDPOINT, or RESUME_URL is missing (value None)
    or set to an empty string, a message is printed and main() returns
    early. The endpoint is registered anyway so a request that slips
    past the guard would be recorded and fail the test.
    """
    if value is None:
        monkeypatch.delenv(variable)
    else:
        monkeypatch.setenv(variable, value)
    response = responses.post(endpoint, status=201, json={"message": "received"})

    main()

    assert len(response.calls) == 0
    assert "missing from" in capsys.readouterr().out
