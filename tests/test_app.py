from types import SimpleNamespace

from app import create_app


def test_home_page_renders():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    response = client.get('/')

    assert response.status_code == 200
    assert b'Rohan Sakalkale' in response.data


def test_contact_route_returns_success(monkeypatch):
    app = create_app()
    app.config.update(TESTING=True, FORMSPREE_ENDPOINT='https://example.com', FIRESTORE_ENABLED=False)

    def fake_forward(endpoint, data):
        assert endpoint == 'https://example.com'
        assert data['name'] == 'Jane'
        return SimpleNamespace(status_code=200)

    monkeypatch.setattr('app.forward_to_formspree', fake_forward)

    client = app.test_client()
    response = client.post('/contact', data={
        'name': 'Jane',
        'email': 'jane@example.com',
        'message': 'Hello there'
    })

    assert response.status_code == 200
    assert response.get_json()['success'] is True
