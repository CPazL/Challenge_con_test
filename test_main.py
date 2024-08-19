import unittest
from unittest.mock import patch, MagicMock
from api.main import main  # Asegúrate de importar tu función main desde el módulo correcto

class TestMainFunction(unittest.TestCase):

    @patch('database_manager.DatabaseManager')
    @patch('drive_manager.GoogleDriveManager')
    @patch('inventory_manager.FileInventory')
    def test_main_function(self, mock_inventory_manager, mock_drive_manager, mock_db_manager):
        # Mock de los métodos y atributos
        mock_db_instance = mock_db_manager.return_value
        mock_connection = MagicMock()
        mock_db_instance.conexion_a_mysql.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        mock_drive_instance = mock_drive_manager.return_value
        mock_drive_instance.autentificacion_drive.return_value = MagicMock()

        mock_inventory_instance = mock_inventory_manager.return_value
        mock_inventory_instance.inventariar_archivos.return_value = None

        # Ejecutar la función main
        main()

        # Verificar que se llamaron los métodos correctos
        mock_db_instance.conexion_a_mysql.assert_called_once()
        mock_db_instance.crear_bd.assert_called_once_with(mock_cursor)
        mock_drive_instance.autentificacion_drive.assert_called_once()
        mock_inventory_instance.inventariar_archivos.assert_called_once_with(mock_cursor, mock_drive_instance.autentificacion_drive.return_value)
        mock_db_instance.cerrar_conexion.assert_called_once_with(mock_cursor)
        mock_connection.close.assert_called_once()
        print("Test de la función main pasado.")

    @patch('database_manager.DatabaseManager')
    def test_main_function_connection_failed(self, mock_db_manager):
        # Simular fallo en la conexión
        mock_db_instance = mock_db_manager.return_value
        mock_db_instance.conexion_a_mysql.return_value = None

        # Ejecutar la función main
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with("No se pudo conectar a la base de datos.")
        print("Test de fallo en conexión a la base de datos pasado.")

if __name__ == '__main__':
    unittest.main()
