# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 17:00:00 2022

@author: Jhonatan Martínez
"""
import logging
from typing import Dict
import pysftp
from .constants import *


class ConnectionSFTP:
    """Permite realizar una conexión a SFTP.
    """

    def __init__(self, setup: Dict[str, str]) -> None:
        """Constructor

        Args:
            setup (Dic[str, str]):
                El diccionario necesita de las siguientes keys:
                - host: Server host.
                - port: Server port.
                - user: SFTP user.
                - password: SFTP password.
        """
        self.__attributes = ['host', 'port', 'user', 'password']
        self.__connection = None
        self.__setup: Dict = setup
        self.__main()

    def __main(self) -> None:
        """Válida que el diccionario contenga los atributos necesarios para que la clase funcione.
        """
        missing = [key for key in self.__attributes if str(key).lower() not in self.__setup.keys()]
        if len(missing) > 0:
            logging.error(MISSING_ATTRIBUTES)
            logging.error(missing)

    def close_connection(self):
        """Cierra la conexión al servidor.
        """
        try:
            if self.__connection is not None:
                self.__connection.close()
                logging.info(CLOSE_CONNECTION)
        except (pysftp.ConnectionException, Exception) as exc:
            logging.error(str(exc),
                          exc_info=True)

    def open_connection(self) -> bool:
        """Establece la conexión al servidor SFTP.\n

        Returns:
            bool: El valor de retorno es True si se realiza con éxito, False en caso contrario.
        """
        self.__connection = None
        try:
            # This is for no use the host keys
            opciones = pysftp.CnOpts()
            opciones.hostkeys = None
            self.__connection = pysftp.Connection(host=self.__setup["host"],
                                                  port=int(self.__setup["port"]),
                                                  username=self.__setup["user"],
                                                  password=self.__setup["password"],
                                                  cnopts=opciones)
            logging.info(ESTABLISHED_CONNECTION, self.__setup["host"])
            return True
        except (pysftp.ConnectionException, Exception) as exc:
            logging.error(str(exc),
                          exc_info=True)
            return False

    def change_path(self, path: str) -> bool:
        """Cambia el directorio en el que se va a trabajar en el servidor SFTP.

        Args:
            path (str): Directorio del SFTP en el que se va a trabajar.

        Returns:
            bool: El valor de retorno es True si se realiza con éxito, False en caso contrario.
        """
        if self.__connection is not None:
            try:
                self.__connection.cwd(path)
                logging.info(CHANGED_PATH, path)
                return True
            except (pysftp.ConnectionException, Exception) as exc:
                logging.error(str(exc),
                              exc_info=True)
                return False
        else:
            logging.error(NO_CONNECTION)
            return False

    def upload_file(self, original_file: str, end_file: str) -> bool:
        """Subir archivos al servidor SFTP.

        Args:
            original_file (str): Recibe la ruta absoluta y el archivo a subir. \n
            end_file (str): Nombre con el que se va a guardar el archivo. \n

        Returns:
             bool: El valor de retorno es True si se realiza con éxito, False en caso contrario.
        """
        if self.__connection is not None:
            try:
                self.__connection.put(original_file, end_file)
                logging.info(UPLOADED_FILE, end_file)
                return True
            except (pysftp.ConnectionException, Exception) as exc:
                logging.error(str(exc),
                              exc_info=True)
                return False
        else:
            logging.error(NO_CONNECTION)
            return False

    def download_file(self, directory: str, filename: str, final_filename: str) -> None:
        """Descargar un archivo de un servidor SFTP.

        Args:
            directory (str): Ruta dónde se van a guardar el archivo a descargar. \n
            filename (str): Nombre del archivo a descargar. \n
            final_filename (str): Nombre con el que se va a guardar el archivo.
        """
        if self.__connection is not None:
            try:
                if self.__connection.isfile(filename):
                    self.__connection.get(filename, directory + "/" + final_filename)
                    logging.info(DOWNLOADED_FILE, final_filename)
            except (pysftp.ConnectionException, Exception) as exc:
                logging.error(str(exc),
                              exc_info=True)
        else:
            logging.error(NO_CONNECTION)

    def download_files(self, directory: str) -> None:
        """Descargar archivos de un servidor SFTP.

        Args:
            directory (str): Ruta dónde se van a guardar los archivos. \n
        """
        try:
            for file in self.__connection.listdir():
                self.download_file(directory, file, file)
        except (pysftp.ConnectionException, Exception) as exc:
            logging.error(str(exc),
                          exc_info=True)
