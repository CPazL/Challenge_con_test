import unittest
from unittest.mock import patch, MagicMock
from googleapiclient.errors import HttpError
from api.notification_manager import MailSenderManager  # Asegúrate de importar tu clase desde el módulo correcto

class TestMailSenderManager(unittest.TestCase):

    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    @patch('googleapiclient.discovery.build')
    def test_autentificacion_mail_exitosa(self, mock_build, mock_creds):
        # Configurar el mock para simular una autenticación exitosa
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        gmail_service = MailSenderManager.autentificacion_mail()
        
        mock_creds.assert_called_once_with('client_secret_mail.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
        mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_creds.return_value)
        self.assertEqual(gmail_service, mock_service)
        print("Test de autenticación exitosa pasado.")

    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    @patch('googleapiclient.discovery.build')
    def test_autentificacion_mail_fallida(self, mock_build, mock_creds):
        # Simular un fallo en la autenticación
        mock_creds.side_effect = Exception("Fallo en la autenticación")
        
        gmail_service = MailSenderManager.autentificacion_mail()
        
        mock_creds.assert_called_once_with('client_secret_mail.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
        self.assertIsNone(gmail_service)
        print("Test de autenticación fallida pasado.")

    @patch('googleapiclient.discovery.build')
    def test_enviar_notificacion_mail_exitoso(self, mock_build):
        # Configurar el mock para simular el envío exitoso de un correo
        mock_service = MagicMock()
        mock_send = mock_service.users.return_value.messages.return_value.send
        mock_send.return_value.execute.return_value = {}

        owner_email = "owner@example.com"
        file_name = "test-file"
        
        with patch('os.getenv', return_value='sender@example.com'):
            MailSenderManager.enviar_notificacion_mail(mock_service, owner_email, file_name)
        
        mock_send.assert_called_once()
        args, kwargs = mock_send.call_args
        body = kwargs['body']
        self.assertIn(owner_email, body['raw'])
        self.assertIn(file_name, body['raw'])
        print("Test de envío exitoso de correo pasado.")
    
    @patch('googleapiclient.discovery.build')
    def test_enviar_notificacion_mail_fallido(self, mock_build):
        # Simular un fallo en el envío del correo
        mock_service = MagicMock()
        mock_send = mock_service.users.return_value.messages.return_value.send
        mock_send.side_effect = HttpError(resp=MagicMock(status=500), content=b'')

        owner_email = "owner@example.com"
        file_name = "test-file"
        
        with patch('os.getenv', return_value='sender@example.com'):
            MailSenderManager.enviar_notificacion_mail(mock_service, owner_email, file_name)
        
        mock_send.assert_called_once()
        print("Test de manejo de error en envío de correo pasado.")
    
    def test_cerrar_sesion(self):
        mock_service = MagicMock()
        MailSenderManager.cerrar_sesion(mock_service)
        mock_service.close.assert_called_once()
        print("Test de cierre de sesión pasado.")

if __name__ == '__main__':
    unittest.main()
