import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("credentials.json")
app = firebase_admin.initialize_app(cred)
DB = firestore.client()
