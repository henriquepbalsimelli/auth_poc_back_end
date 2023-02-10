from dataclasses import asdict, dataclass, field
import os
from typing import List
import google.oauth2.credentials
import google_auth_oauthlib.flow

@dataclass
class Auth():

    def __init__(self):
        self.authorization_type = os.getenv('AUTHORIZATION_TYPE')

    def authorize(self) -> dict:
        if self.authorization_type == 'LIB':
            authorization = self.authorize_by_lib()
        else:
            authorization = self.authorize_by_http()

        return authorization

    def authorize_by_lib(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=[
            'https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/gmail.send'
            ])

        flow.redirect_uri = 'http://localhost:5000/get/token'

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true'
            )
        
        return {
            'url': authorization_url,
            'state': state
        }
    
    def authorize_by_http(self) -> dict:
        return asdict(self)
    
    
