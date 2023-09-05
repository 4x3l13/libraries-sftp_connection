Librería para conectar a SFTP

Por Jhonatan Martínez - jhonatanmartinez130220@gmail.com

Librería te permite descargar o cargar archivos al SFTP:

Para utilizarla solo necesitas pasar un diccionario con los datos solicitados, estos se pueden ver al invocar la clase ConnectionSFTP.

💡 Prerequisitos
Python==3.8.9,
pysftp==0.2.9

📚 Ejemplo de uso

    from SFTP import ConnectionSFTP
    
    sftp = ConnectionSFTP(setup=my_dictionary)
    
    sftp.get_connection()
    
    sftp.change_path(path='/home')

    sftp.download_files(directory='C://home')

    sftp.close_connection()
