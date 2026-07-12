# Static Personal Website

This project now runs as a small Flask application with the same website content and tracking scripts, while keeping the contact form routed through Formspree and optionally storing submissions in Firestore.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The site is available at http://127.0.0.1:8000/.

## Environment variables

Copy [.env.example](.env.example) to .env and configure the values as needed.

For production, set at least:

- `SECRET_KEY`
- `FORMSPREE_ENDPOINT`
- `FIRESTORE_ENABLED`
- `GOOGLE_CLOUD_PROJECT` or `FIRESTORE_PROJECT_ID`

- `FORMSPREE_ENDPOINT`: Formspree endpoint used for submissions
- `FIRESTORE_ENABLED`: set to `true` to enable Firestore persistence
- `GOOGLE_CLOUD_PROJECT` or `FIRESTORE_PROJECT_ID`: GCP project id
- `FIRESTORE_COLLECTION`: Firestore collection name

## Deploy to Cloud Run

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/portfolio-website
gcloud run deploy portfolio-website --image gcr.io/PROJECT_ID/portfolio-website --platform managed --region us-central1
```
