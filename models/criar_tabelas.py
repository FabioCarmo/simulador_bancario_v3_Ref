
from models.conexaodb import Conexao

# Criar as tabelas 'clientes', 'contas', 'saldo' e 'transacao' com suas colunas e atributos
def criar_tabela():
    conexao = Conexao()
    conexaodb = conexao.conectar()
    cursor = conexao.cursor

    try:
        cursor.executescript("CREATE TABLE clientes (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome VARCHAR(50) NOT NULL, cpf VARCHAR(15) NOT NULL UNIQUE, data_nascimento DATE NOT NULL, endereco VARCHAR(100) NOT NULL); \
        CREATE TABLE contas (ID INTEGER NOT NULL, cpf VARCHAR NOT NULL UNIQUE, agencia VARCHAR(4) NOT NULL, conta INTEGER(5) NOT NULL); \
        CREATE TABLE saldo (ID INTEGER NOT NULL, saldo FLOAT(12)  NOT NULL DEFAULT 0.00); \
        CREATE TABLE transacao(ID INTEGER NOT NULL, tipo VARCHAR(10), valor FLOAT(12) NOT NULL, data DATE);")
        conexaodb.commit()
    except:
        conexaodb.rollback()
        return False
    
if __name__ == "__main__":
    criar_tabela()