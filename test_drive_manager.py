import unittest
from unittest.mock import patch, MagicMock
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from api.drive_manager import GoogleDriveManager  # Asegúrate de importar tu clase desde el módulo correcto

class TestGoogleDriveManager(unittest.TestCase):
    
    @patch('os.path.exists')
    @patch('google.oauth2.credentials.Credentials.from_authorized_user_file')
    @patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file')
    def test_autentificacion_drive(self, mock_flow, mock_creds_from_file, mock_path_exists):
        # Simular que el archivo 'token.json' existe
        mock_path_exists.return_value = True
        mock_creds = MagicMock(spec=Credentials)
        mock_creds.valid = True
        mock_creds_from_file.return_value = mock_creds
        
        manager = GoogleDriveManager()
        creds = manager.autentificacion_drive()
        
        self.assertEqual(creds, mock_creds)
        print("Test de autenticación de Google Drive pasado.")
    
    @patch('googleapiclient.discovery.build')
    def test_visibilidad_publico_a_privado(self, mock_build):
        mock_service = mock_build.return_value
        mock_service.permissions.return_value.delete.return_value.execute = MagicMock()
        
        file = {'id': 'test-file-id'}
        manager = GoogleDriveManager()

        with patch.object(manager, 'obtienePermisosRegistrados', return_value=[{'id': 'perm-id', 'type': 'anyone'}]):
            manager.visibilidad_publico_a_privado(file, mock_service)

        mock_service.permissions().delete.assert_called_with(fileId='test-file-id', permissionId='perm-id')
        
