
# Importar base de dados sqlite
import sqlite3
from pathlib import Path

class Conexao():

    def __init__(self):
        self._PATH = Path(__file__).parent.resolve() # Diretorio do projeto
        self._enderecodb = str(self._PATH / "bancodasnotas.sqlite3")
        self._conectado = False

    def conectar(self):
        try:
            self._conexaodb = sqlite3.connect(self._enderecodb) # conecta com db
            self._conectado = True
            return self._conexaodb
        except sqlite3.Error as exc:
            return exc

    # Encerra a conexao com a base de dados
    def fechar(self):
        if (self._conectado):
            self._conexaodb.close()
            self._conectado = False
            self._conexaodb = None


    # retorna metodo cursor
    @property   
    def cursor(self):
        if (self._conectado): 
            return self._conexaodb.cursor()
        