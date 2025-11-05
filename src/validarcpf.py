
# Importar biblioteca regex
import re 

def filtrarcpf(cpf):
    cpf = cpf.strip()
    cpf = re.sub(r"\D", '', cpf) # remove os caracteres não numericos
    
    # remove os valores do tipo string da variavel
    if cpf.isdigit() == 1:
        cpf = cpf

    # Valida se a quantidades de digitos é igual a 11
    if not re.fullmatch(r'\d{11}', cpf):
        return False

    # Valida se os numeros são iguais
    if cpf == cpf[0] * 11:
        return False

    return cpf # Retorna o cpf com alteracoes ou false
