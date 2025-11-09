
# Conjunto de classes usado no projeto

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.clientes = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
