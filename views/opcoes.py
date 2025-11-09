
# Importar modulo de identacao
from src.cliente import Cliente, PessoaFisica
from src.conta import Conta, ContaCorrente
from src.saque import Saque
from src.deposito import Deposito
from src.historico import Historico
from models.dominio import DbBanco
from src.validarcpf import filtrarcpf

db = DbBanco()

# Retorna os dados de Pessoa Fisica do usuario
def filtrar_cliente(cpf):
    cpf = (cpf,)
    clientes_filtrados = db.listar_dados(indice=cpf, tabela="clientes", condicao="cpf")
    return clientes_filtrados if clientes_filtrados else None

# Retorna os dados de conta do usuario
def recuperar_conta_cliente(id):
    id = (id,)
    contas_filtradas = db.listar_dados(indice=id, tabela="contas", condicao="ID")
    return contas_filtradas if contas_filtradas else None

# Realiza operacao de deposito
def depositar(clientes, contas):
    cpf = filtrarcpf(input("Informe seu CPF para continuar: "))

    if cpf != clientes['cpf']:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    if not contas:
        return

    valor = float(input("Informe o valor do depósito: ").strip())

    # Recupera a instancia do objeto Conta e PessoaFisica
    cliente = clientes['Cliente'] # PessoaFisica
    conta = contas['Conta'] # Conta
    saldo_atual = conta.saldo + valor
    # Atualiza a operacao de deposito no objeto e atualiza o saldo
    cliente.realizar_transacao(conta, Deposito(valor))

    # Atualiza o saldo no DB
    dados = (clientes['id'], saldo_atual)
    saldo(dados)

# Realiza operacao de saque
def sacar(clientes, contas):
    cpf = filtrarcpf(input("Informe seu CPF para continuar: "))

    if cpf != clientes['cpf']:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    if not contas:
        return

    valor = float(input("Informe o valor do saque: ").strip())
    
    # Recupera a instancia do obj Conta e PessoaFisica
    conta = contas['Conta'] # Conta
    cliente = clientes['Cliente'] # PessoaFisica
    saldo_atual = conta.saldo - valor
    # Atualiza a operacao de saque no objeto e atualiza o saldo
    transacao = cliente.realizar_transacao(conta, Saque(valor))

    # Atualiza o saldo no DB
    dados = (clientes['id'], saldo_atual)
    saldo(dados)

# Exibir o historico de transacoes do usuario
def exibir_extrato(clientes, contas):

    if not clientes:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    if not contas:
        return

    print("\n================ EXTRATO ================")
    transacoes = Historico().transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    # Recupera o obj Conta
    conta = contas['Conta']
    saldo = conta.saldo # Recupera o saldo

    print(extrato)
    print(f"\nSaldo:\tR$ {saldo:.2f}")

    press = input("Press Enter ou ok").strip()
    if len(press) > 0:
        return
    print("==========================================")

# Criar novo cliente
def criar_cliente(clientes: list):
    cpf = input("Informe o CPF (somente os 11 digitos): ")
    cpf = filtrarcpf(cpf)

    if cpf == False:
        print("Cpf invalido !")
        return

    cliente = filtrar_cliente(cpf)

    if cliente != None:
        if cpf == cliente[2]:
            print("\n@@@ Já existe cliente com esse CPF! @@@")
            return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (aaaa-mm-dd): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    # Instancia o objeto PessoaFisica
    clienteobj = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    dados_cliente = (nome, cpf, data_nascimento, endereco)
    res_db = db.inserir_cliente(dados_cliente) # Metodo do db para inserir registros
    
    if res_db == False:
        print("Erro ao cadastrar cliente !")
        return

    cliente = filtrar_cliente(cpf)
    clientes.update({
                'id': cliente[0], 
                'nome': clienteobj.nome, 
                'cpf': clienteobj.cpf, 
                'Cliente': clienteobj
            })

    print("\n=== Cliente criado com sucesso! ===")

# Criar nova conta bancaria do usuário
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cpf = filtrarcpf(cpf)

    if cpf == False:
        print("Cpf invalido !")
        return

    if not clientes:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    # Instancia o objeto com metodo de classe e passa a variavel e posteriormente a lista
    contaobj = ContaCorrente.nova_conta(cliente=clientes, numero=numero_conta)

    agencia = int(1) # Obter o numero da agencia
    dados = (clientes['id'], clientes['cpf'], contaobj.agencia, contaobj.numero) # Cliente[0] armazena o id do cliente
    resultado_db = db.inserir_conta(dados) # Metodo do db para inserir registros

    if resultado_db == False:
        print("Erro ao cadastrar conta !")
        return
    
    dados = (clientes['id'], 0)
    saldo(dados)
    contaobj.saldo_atual(0) # Atualiza o saldo atual no obj

    contas.update({
                'id': clientes['id'], 
                'agencia': contaobj.agencia,
                'numero': contaobj.numero, 
                'Conta': contaobj
            })

    print("\n=== Conta criada com sucesso! ===")

# Atualiza o saldo da conta
def saldo(dados):
    adicionar_saldo = db.inserir_saldo(dados)
    return adicionar_saldo

# Realiza o login e instancia o obj
# Conta e PessoaFisica e passa para a lista para novas operacoes
def login(clientes: list, contas: list):
    cpf = input("Digite seu cpf: ")
    cpf = filtrarcpf(cpf)

    if cpf == False:
        print("Cpf invalido !")
        return

    cliente = filtrar_cliente(cpf)

    if cliente == None:
        print("\n@@@Cliente não possui conta!")
        return

    conta = recuperar_conta_cliente(cliente[0])

    # Instancia o objeto PessoaFisica e passa a variavel e posteriormente a lista
    clienteobj = PessoaFisica(nome=cliente[1], data_nascimento=cliente[3], cpf=cliente[2], endereco=cliente[4])
    clientes.update({
                'id': cliente[0], 
                'nome': clienteobj.nome, 
                'cpf': clienteobj.cpf, 
                'Cliente': clienteobj
                })

    if conta != None:
        contaobj = ContaCorrente(numero=conta[3], cliente=clientes)
        contas.update({
                  'id': clientes['id'],
                  'agencia': contaobj.agencia, 
                  'numero': contaobj.numero, 
                  'Conta': contaobj
                  })
        
        conta_saldo = db.listar_dados(indice=(clientes['id'],), tabela="saldo", condicao="ID")
        contaobj.saldo_atual(conta_saldo[1]) # Atualiza o saldo atual no obj

    print(f"Bem-vindo de volta, {clientes['nome']}.")

# Excluir Registros do usuario
def excluir_registro(clientes, contas):

    if not clientes:
        print("Cliente não encontrado !")
        return 

    while True:
        opcao = input("Deseja excluir todos os seus dados ? Press 's' ou 'n'").strip().lower()

        if opcao == 's':
            TABELAS = ['clientes', 'contas', 'saldo', 'transacao']
            for i in range(0, 3):
                excluir_registro = db.excluir_registro(indice=(clientes['id'],), tabela=TABELAS[i])

            if excluir_registro == False:
                print("Erro ao excluir dados !")
                return
            else:
                print("Seus dados foram excluidos com sucesso!")
                clientes.clear()
                contas.clear()
                return 
            
        elif opcao == 'n':
            return

        else:
            print("Opção invalida ")
            continue
        