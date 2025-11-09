import textwrap

def menu(clientes, contas):

    opcoes_menu_login = ['[1]\tDepositar', '[2]\tSacar', '[3]\tExtrato', '[4]\tAbrir Conta', \
                         '[9]\tExcluir meus dados', '[0]\tSair\n=>', '[1]\tNova Conta', '[2]\tLogin', '[0]\tSair\n=>']
    menu = ""

    if not clientes:
        opcoes_validas = opcoes_menu_login[6:]

    else:
        opcoes_validas = opcoes_menu_login[:6]

    # Se o usuario tiver conta apaga a posicao de novo usuario da lista de opcoes
    if contas:
         del opcoes_validas[3]

    for valor in opcoes_validas:
        menu += valor + '\n'

    return input(textwrap.dedent(menu)).strip()