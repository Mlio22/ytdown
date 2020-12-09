from pydrive.auth import GoogleAuth
from pathlib import Path
import os


def authenticate():
    credentials_path = Path(__file__).parent
    gauth = GoogleAuth(os.path.join(credentials_path, "settings.yaml"))

    # Try to load saved client credentials
    gauth.LoadCredentialsFile(os.path.join(credentials_path, "credentials.json"))

    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile(os.path.join(credentials_path, 'credentials.json'))

    return gauth

