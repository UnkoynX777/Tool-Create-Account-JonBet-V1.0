import os
import sys
import io
from colorama import Fore

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

blue = Fore.BLUE
green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
roxo = Fore.MAGENTA
reset = Fore.RESET

credentials_path = './[UNKOYNX7]/[ONLY-CREATE]/credentials.txt'

if not os.path.exists(credentials_path):
    print(f"{red}[ERROR]{reset} {roxo}O arquivo de credenciais não foi encontrado.{reset}")
else:
    with open(credentials_path, 'r', encoding='utf-8') as file:
        accounts = file.readlines()

    seen_cpfs = set()
    updated_accounts = []

    for account in accounts:
        stripped_account = account.strip()
        if stripped_account:
            cpf = stripped_account.split(':')[0]
            if cpf not in seen_cpfs:
                seen_cpfs.add(cpf)
                updated_accounts.append(stripped_account)
                print(f"{yellow}[INFO]{reset} {roxo}({cpf}) - Adicionado à lista de dados únicas.{reset}")

    if updated_accounts:
        with open(credentials_path, 'w', encoding='utf-8') as file:
            file_content = '\n'.join(updated_accounts).rstrip()
            file.write(file_content)
        
        print(f"{green}[SUCCESS]{reset} {roxo}Dados foram atualizados.{reset}")
    else:
        print(f"{yellow}[WARNING]{reset} {roxo}O arquivo está vazio.{reset}")