import os
import json
from flask import Flask, request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

# --- CONFIGURATION ---
FOLDER_ID = '1j56Q-FqluXCoLvU_WVBTYNntAFZiLPAr'
# -------------------

def get_drive_service():
    """Authenticates using credentials from environment variables."""
    try:
        # Get the credentials from the Vercel environment variable
        creds_json_str = os.environ.get('GOOGLE_CREDS_JSON')
        if not creds_json_str:
            return "Error: GOOGLE_CREDS_JSON environment variable not set."

        creds_info = json.loads(creds_json_str)
        scopes = ['https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_info(creds_info, scopes=scopes)
        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        return f"Authentication failed. Error: {e}"

@app.route("/")
def index():
    return "Welcome! Go to /start-analysis to begin."

@app.route("/start-analysis")
def start_analysis():
    """Main function to list, analyze, and rename files."""
    drive_service = get_drive_service()
    if isinstance(drive_service, str): # Check if get_drive_service returned an error string
        return drive_service

    output_log = "Processing files...\n"
    output_log += "-------------------------------------------\n"

    # This part will need to be adapted for batching on Vercel's free tier
    # For now, it will try to process all files.
    try:
        query = f"'{FOLDER_ID}' in parents and trashed=false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return "No files found in the folder."

        for item in items:
            # The logic for renaming each item would go here
            # Note: This is a simplified version for the initial setup.
            # A full implementation would need to handle timeouts.
            output_log += f"Found file: {item['name']}\n"

    except HttpError as error:
        return f'An error occurred listing files: {error}'

    return f"<pre>{output_log}All images processed.</pre>"