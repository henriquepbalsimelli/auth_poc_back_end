import os
import json
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow

from datetime import datetime, timedelta
from dataclasses import dataclass
from flask import redirect
from typing import List
from urllib.parse import urlencode
from exceptions.NetworkException import NetworkException

from services.auth.dto.GoogleAuthDto import GoogleAuthDto


@dataclass
class AuthService():

    __authorization_type: str
    __google_client_id: str
    __google_client_api_secret: str

    def __init__(self):
        self.__authorization_type = os.getenv('AUTHORIZATION_TYPE')
        self.__google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.__google_client_api_secret = os.getenv('GOOGLE_CLIENT_API_SECRET')

    def authorize(self) -> dict:
        if self.__authorization_type == 'LIB':
            authorization = self.__authorize_by_lib()
        else:
            authorization = self.__authorize_by_http()

        return authorization
    
    def get_token(self, authorization_code: str, code: str=None, state: str=None):
        
        return self.__get_token_by_http(authorization_code=authorization_code)
        

    def __authorize_by_lib(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=[
            'https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/gmail.send'
            ])

        # Lembrando que todas as url de redirect devem estar habilitadas no projeto do Google Cloud Plataform
        # Além disso, essas urls precisam ser iguais na obtenção do token de acesso e no token de autorização
        flow.redirect_uri = 'http://localhost:5000/get/token'

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
            )
        return authorization_url
    
    def __authorize_by_http(self) -> str:
        scopes = [
            'https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/gmail.send'
        ]
        
        params = {
            'client_id': self.__google_client_id,
            'scope': ' '.join(scopes),
            'include_granted_scopes': 'true',
            'response_type': 'code',
            'access_type': 'offline',
            'redirect_uri': 'http://localhost:5000/get/token'
        }

        # redirect authorization to google
        url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params)
        redirect_data = redirect(location=url, code=302)
        return redirect_data
    
    
    
    def __get_token_by_http(self, authorization_code: str):
        body = {
            'client_id': self.__google_client_id,
            'client_secret': self.__google_client_api_secret,
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:5000/get/token'
        }

        response = requests.post(url='https://oauth2.googleapis.com/token', json=body)
        self.__handle_response_errors(response=response)

        json_data = response.json()

        token_expiration = datetime.today() + timedelta(seconds=json_data.get('expires_in'))
        return GoogleAuthDto(authorization_code=authorization_code,
                            access_token=json_data.get('access_token'),
                            refresh_token=json_data.get('refresh_token'),
                            expiration=token_expiration)
    
    def __handle_response_errors(self, response):
        
        if 400 <= response.status_code < 600:
            try: 
                payload = json.loads(response.content)
            except: 
                payload = {'error': response.text}

            raise NetworkException(message=f'Request Error from {response.url}',
                                   status_code=response.status_code,
                                   payload=payload)
                    
    def revoke(self, token):
        response = requests.post(url=f'https://oauth2.googleapis.com/revoke?token={token}')
        return response