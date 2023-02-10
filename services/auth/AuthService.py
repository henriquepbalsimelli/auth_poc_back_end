import os
import google.oauth2.credentials
import google_auth_oauthlib.flow

from dataclasses import dataclass
from flask import redirect
from typing import List
from urllib.parse import urlencode


@dataclass
class AuthService():

    __authorization_type: str
    __google_client_id: str

    def __init__(self):
        self.__authorization_type = os.getenv('AUTHORIZATION_TYPE')
        self.__google_client_id = os.getenv('GOOGLE_CLIENT_ID')

    def authorize(self) -> dict:
        if self.__authorization_type == 'LIB':
            authorization = self.__authorize_by_lib()
        else:
            authorization = self.__authorize_by_http()

        return authorization

    def __authorize_by_lib(self):
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
    
    def __authorize_by_http(self) -> str:
        scopes = [
            'https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/gmail.send'
        ]
        
        params = {
            "client_id": self.__google_client_id,
            "scope": ' '.join(scopes),
            "include_granted_scopes": 'true',
            "response_type": 'code',
            "access_type": 'offline',
            "redirect_uri": 'http://localhost:5000/users/authorize'
        }

        # redirect authorization to google
        url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params)
        return redirect(location=url)
    
    
