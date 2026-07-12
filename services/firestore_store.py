import os
from datetime import datetime, timezone


class FirestoreStore:
    def __init__(self, project_id=None, collection_name=None):
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('FIRESTORE_PROJECT_ID', '')
        self.collection_name = collection_name or os.getenv('FIRESTORE_COLLECTION', 'contact_submissions')

    def save_submission(self, data):
        if not self.project_id:
            raise RuntimeError('Firestore project ID is not configured')

        from google.cloud import firestore

        client = firestore.Client(project=self.project_id)
        payload = {
            **data,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'source': 'portfolio-website'
        }
        client.collection(self.collection_name).add(payload)
        return True
