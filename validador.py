
import re

def validar_nif(valor):
    return bool(re.fullmatch(r'\d{9}', valor))

def validar_niss(valor):
    return bool(re.fullmatch(r'\d{11}', valor))

def validar_iban(valor):
    return bool(re.fullmatch(r'PT50\d{21}', valor))
