
from pathlib import Path
from models.conexaodb import Conexao

# Classe DbBanco para realizar operacoes na base de dados

class DbBanco():

    def __init__(self):
        self._conexao = Conexao()
        self._conexao = self._conexao.conectar()
        self._cursor = self._conexao.cursor()
    
    # Inserir registros na tabela 'clientes'
    def inserirCliente(self, dados):
        try:
            self._cursor.execute("INSERT INTO clientes(nome, cpf, data_nascimento, endereco) VALUES(?,?,?,?)", dados)
            self._conexao.commit()
            return True
        except:
            self._conexao.rollback()
            return False
    
    # inserir registros na tabela 'contas'
    def inserirConta(self, dados):
        try:
            self._cursor.execute("INSERT INTO contas(ID, cpf, agencia, conta) VALUES(?,?,?,?)", dados)
            self._conexao.commit()
            return True
        except:
            self._conexao.rollback()
            return False
    
    def inserirSaldo(self, indice, valor=float(0.00)):
        try: 
            self._cursor.execute("INSERT INTO saldo(ID, saldo) VALUES(?,?);", (indice, valor))
            self._conexao.commit()
            return True
        except:
            self._conexao.rollback()
            return False
    
    def listarSaldo(self, indice):
        try:
            self._cursor.execute("SELECT saldo FROM saldo WHERE ID = ?;", indice)
            return self._cursor.fetchone()
        except:
            self._conexao.rollback()
            return False
    
    # Retornar os dados da tabela clientes
    def listarClientes(self, indice = None):
        if not indice:
            return None
        else:
            self._cursor.execute("SELECT * FROM clientes WHERE cpf = ?", indice)
            return self._cursor.fetchone()

    # Retornar os dados da tabela contas
    def listarContas(self, indice=None):
        if not indice:
            return None
        else:
            if (indice):
                self._cursor.execute("SELECT * FROM contas WHERE ID = ?;", indice)
                return self._cursor.fetchone()
    
    # Excluir registro por chave primaria
    def excluir_registro(self, indice):

        tabelas = ["clientes", "contas", "transacao", "saldo"]
        try:
            for tabela in tabelas:
                self._cursor.execute(f"DELETE FROM {tabela} WHERE ID = ?;", (indice,))

            self._conexao.commit()
            return True
        except Exception:
            self._conexao.rollback()
            return False
        
    def normalizar_dados(self):
        self._cursor.execute("DROP TABLE ")
        self._conexao.commit()