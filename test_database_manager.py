#Unittest define un conjunto de pruebas
import unittest
#Sirve para pruebas unitarias que requieren la simulación (mocking) de objetos y comportamientos que no se pueden probar directamente en un entorno de prueba.
from unittest.mock import patch, MagicMock

from mysql.connector import connect
from mysql.connector.errors import Error as MySQLError
from api.database_manager import DatabaseManager  



class TestDatabaseManager(unittest.TestCase):
    #reemplaza el cursor original con un mock (un cursor simulado) 
    @patch('mysql.connector.connect')
    
    def test_conexion_a_mysql_exitosa(self, mock_connect):
        # Configurar el mock para simular una conexión exitosa
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        db_manager = DatabaseManager()
        conn = db_manager.conexion_a_mysql()
        
        mock_connect.assert_called_once()
        self.assertIsNotNone(conn)
        print("Conexión a MySQL exitosa test pasada.")
    
    @patch('mysql.connector.connect')
    def test_conexion_a_mysql_fallida(self, mock_connect):
        # Configurar el mock para simular un error de conexión
        mock_connect.side_effect = MySQLError("Error al conectar a MySQL")
        
        db_manager = DatabaseManager()
        conn = db_manager.conexion_a_mysql()
        
        self.assertIsNone(conn)
        print("Test de conexión fallida a MySQL pasada.")
    
    def test_crear_bd(self):
        mock_cursor = MagicMock()
        db_manager = DatabaseManager()
        
        # Simular la creación de la base de datos y tablas
        db_manager.crear_bd(mock_cursor)
        
        mock_cursor.execute.assert_any_call(f"CREATE DATABASE {database_name};")
        mock_cursor.execute.assert_any_call(f"USE {database_name};")
        print("Test de creación de BD y tablas pasado.")
    
    def test_crear_usuario(self):
        mock_cursor = MagicMock()
        db_manager = DatabaseManager()
        
        with patch('password_utils.PasswordUtils.generate_new_password', return_value='password123'):
            db_manager.crear_usuario(mock_cursor)
        
        mock_cursor.execute.assert_called_with(f"CREATE USER '{access_user}'@'%' IDENTIFIED BY 'password123';")
        print("Test de creación de usuario pasado.")
    
    def test_usuario_permisos(self):
        mock_cursor = MagicMock()
        db_manager = DatabaseManager()
        
        db_manager.usuario_permisos(mock_cursor)
        
        mock_cursor.execute.assert_any_call(f"GRANT CREATE ON {database_name}.* TO '{access_user}'@'%';")
        mock_cursor.execute.assert_any_call(f"GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT ON `{table_name_files_all}`.* TO '{access_user}'@'%';")
        mock_cursor.execute.assert_any_call(f"GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT ON `{table_name_files_public}`.* TO '{access_user}'@'%';")
        mock_cursor.execute.assert_called_with("FLUSH PRIVILEGES;")
        print("Test de asignación de permisos pasado.")
    
    def test_elimina_usuario(self):
        mock_cursor = MagicMock()
        db_manager = DatabaseManager()
        
        db_manager.elimina_usuario(mock_cursor)
        
        mock_cursor.execute.assert_called_with(f"DROP USER '{access_user}'@'%';")
        print("Test de eliminación de usuario pasado.")

if __name__ == '__main__':
    unittest.main()
