import unittest
from unittest.mock import patch, mock_open, MagicMock
from api.password_utils import PasswordUtils  # Asegúrate de importar tu clase desde el módulo correcto

class TestPasswordUtils(unittest.TestCase):

    @patch('random.choice')
    def test_generate_new_password(self, mock_choice):
        # Simular la selección de caracteres aleatorios
        mock_choice.side_effect = lambda x: x[0]  # Siempre seleccionar el primer carácter disponible
        
        password_utils = PasswordUtils()
        length = 8
        expected_password = 'Aa1!Aa1!'
        
        with patch.object(password_utils, 'save_password_to_env') as mock_save_password:
            generated_password = password_utils.generate_new_password(length)
        
        self.assertEqual(generated_password, expected_password)
        mock_save_password.assert_called_once_with(expected_password)
        print("Test de generación de nueva contraseña pasado.")

    @patch('builtins.open', new_callable=mock_open, read_data="DB_access_user_PASS=oldpassword\n")
    def test_save_password_to_env_update_existing(self, mock_file):
        new_password = "newpassword"
        
        PasswordUtils.save_password_to_env(new_password)
        
        mock_file.assert_called_with('.env', 'r')
        mock_file().write.assert_called_with("DB_access_user_PASS=newpassword\n")
        print("Test de actualización de contraseña en .env pasado.")

    @patch('builtins.open', new_callable=mock_open, read_data="SOME_OTHER_ENV_VAR=somevalue\n")
    def test_save_password_to_env_add_new(self, mock_file):
        new_password = "newpassword"
        
        PasswordUtils.save_password_to_env(new_password)
        
        mock_file.assert_called_with('.env', 'r')
        mock_file().write.assert_called_with("DB_access_user_PASS=newpassword\n")
        print("Test de agregar nueva contraseña en .env pasado.")

if __name__ == '__main__':
    unittest.main()
