
# Importar base de dados sqlite
import sqlite3
from pathlib import Path

class Conexao():

    def __init__(self):
        self._PATH = Path(__file__).parent.resolve() # Diretorio do projeto
        self._enderecodb = str(self._PATH / "bancodasnotas.sqlite3")
        self._conectado = False
        self._cursordb = None

    # Conectar com a base de dados sqlite3
    def conectar(self):
        try:
            self._conexaodb = sqlite3.connect(self._enderecodb, timeout=float(3)) # conecta com db
            self._conectado = True
            self._cursordb = self._conexaodb.cursor()
            return self._conexaodb
        except:
            return False

    # Encerra a conexao com a base de dados
    def fechar(self):
        if (self._conectado):
            self._conexaodb.close()
            self._conectado = False
            self._conexaodb = None


    # retorna atributo com metodo cursor
    @property   
    def cursor(self):
        return self._cursordb
        
    # retorna atributo conectado
    @property   
    def dbconectado(self):
        return self._conectado

if __name__ == '__main__':
    Conexao().conectar()