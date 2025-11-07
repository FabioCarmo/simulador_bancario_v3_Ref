
from pathlib import Path
from models.conexaodb import Conexao

# Classe DbBanco para realizar operacoes na base de dados

class DbBanco(Conexao):

    def __init__(self):
        super().__init__() # Instancia objeto da superclasse
        self._conexao = super().conectar()
        self._cursor = super().cursor
        self._conectado = super().dbconectado
        self._TABELAS = ['clientes', 'contas', 'saldo', 'transacao']
    
    # Inserir registros na tabela 'clientes'
    def inserir_cliente(self, dados: tuple):
        try:
            self._cursor.execute("INSERT INTO clientes(nome, cpf, data_nascimento, endereco) \
                                 VALUES(?,?,?,?)", dados)
            self._conexao.commit()
            return True
        except:
            self._conexao.rollback()
            return False
    
    # inserir registros na tabela 'contas'
    def inserir_conta(self, dados: tuple):
        try:
            self._cursor.execute("INSERT INTO contas(ID, cpf, agencia, conta) VALUES(?,?,?,?)", dados)
            self._conexao.commit()
            return True
        except:
            self._conexao.rollback()
            return False
    
    # Inserir registros na tabela 'saldo'
    def inserir_saldo(self, dados: tuple):
        try: 
            self.excluir_registro(indice=(dados[0],), tabela='saldo')
            self._cursor.execute("INSERT INTO saldo(ID, saldo) VALUES(?,?);", dados)
            self._conexao.commit()
            return True
        except:
            self._conexao.rollback()
            return False
        
    # Inserir registros na tabela 'transacao'
    def inserir_transacao(self, dados: tuple):
        try: 
            self._cursor.execute("INSERT INTO transacao(ID, tipo, valor, data) VALUES(?,?,?,?);", dados)
            self._conexao.commit()
            return True
        except:
            self._conexao.rollback()
            return False
    
    # Realiza a consulta das tabelas por chave primaria
    def listar_dados(self, indice: tuple, tabela=None, condicao=None):
        if tabela == None:
            return

        tab_encontrado = False
        for ind in range(len(self._TABELAS)):
            if self._TABELAS[ind] in tabela:
                tab_encontrado = True
        
        if tab_encontrado == False:
            return
        
        try:
            self._cursor.execute(f"SELECT * FROM {tabela} WHERE {condicao} = ?;", indice)
            return self._cursor.fetchone()
        except:
            self._conexao.rollback()
            return False
    
    # Excluir registro por chave primaria
    def excluir_registro(self, indice: tuple, tabela=None):
        try:     
            self._cursor.execute(f"DELETE FROM {tabela} WHERE ID = ?;", indice)
            self._conexao.commit()
            return True
        except Exception:
            self._conexao.rollback()
            return False
    
    # Deleta a tabela do banco
    def normalizar_dados(self, tabela=None):
        try:
            self._cursor.execute(f"DROP TABLE {tabela}")
            self._conexao.commit()
        except:
            self._conexao.rollback()
            return False