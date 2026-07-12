import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from services.firestore_store import FirestoreStore

load_dotenv()


def forward_to_formspree(endpoint, payload):
    response = requests.post(endpoint, data=payload, timeout=10)
    response.raise_for_status()
    return response


def create_app():
    app = Flask(__name__, static_folder='.', static_url_path='/static', template_folder='templates')
    app.config.from_mapping(
        FORMSPREE_ENDPOINT=os.getenv('FORMSPREE_ENDPOINT', 'https://formspree.io/f/xykqqwky'),
        FIRESTORE_ENABLED=os.getenv('FIRESTORE_ENABLED', 'false').lower() in {'1', 'true', 'yes', 'on'},
        FIRESTORE_COLLECTION=os.getenv('FIRESTORE_COLLECTION', 'contact_submissions'),
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key')
    )

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/success')
    def success():
        return render_template('success.html')

    @app.route('/contact', methods=['POST'])
    def contact():
        payload = request.form.to_dict()

        try:
            forward_to_formspree(app.config['FORMSPREE_ENDPOINT'], payload)
        except requests.RequestException as exc:
            app.logger.exception('Formspree submission failed')
            return jsonify(success=False, error='Unable to submit form right now.'), 502

        if app.config.get('FIRESTORE_ENABLED'):
            try:
                FirestoreStore(collection_name=app.config['FIRESTORE_COLLECTION']).save_submission({
                    **payload,
                    'submitted_at': datetime.now(timezone.utc).isoformat()
                })
            except Exception:
                app.logger.exception('Firestore persistence failed')

        return jsonify(success=True)

    @app.route('/healthz')
    def healthz():
        return jsonify(status='ok')

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8000')), debug=False)
