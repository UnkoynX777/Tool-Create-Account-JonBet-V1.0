import json
import os
import sys
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
import io
import random
import string

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

red = Fore.RED
green = Fore.GREEN
purple = Fore.MAGENTA
yellow = Fore.YELLOW
reset = Fore.RESET

config_path = './config.json'
profiles_create_path = './[UNKOYNX7]/[ONLY-CREATE]/profilesCreate.txt'
credentials_2_path = './[UNKOYNX7]/[ONLY-CREATE]/credentials-2.txt'
credentials_path = './[UNKOYNX7]/[ONLY-CREATE]/credentials.txt'
proxys_path = './[UNKOYNX7]/[ONLY-CREATE]/proxys.txt'
maxUserPath = './[UNKOYNX7]/maxUser.txt'

def verificar_max_user():
    try:
        with open(maxUserPath, 'r') as file:
            conteudo = file.read().strip()
            
            if conteudo == 'True':
                return
            else:
                pass
                
    except FileNotFoundError:
        print(f"O arquivo {maxUserPath} não foi encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

if not os.path.exists(config_path):
    print(f"{red}[ERROR]{reset} {purple}O arquivo de configuração não foi encontrado.{reset}", end='')
    sys.stdout.flush()
    sys.exit(1)

with open(config_path) as config_file:
    config = json.load(config_file)

def get_accounts():
    if not os.path.exists(credentials_2_path):
        print(f"{red}[ERROR]{reset} {purple}O arquivo de perfis criados não foi encontrado.{reset}", end='')
        sys.stdout.flush()
        sys.exit(1)

    with open(credentials_2_path, 'r', encoding='utf-8') as file:
        accounts = file.readlines()

    accounts = [line.strip() for line in accounts if line.strip()]

    if not accounts:
        return []

    extracted_data = []
    for account in accounts:
        parts = account.split(' - ')
        if len(parts) >= 3:
            cpf = parts[0].strip()
            proxy_info = parts[1].strip()
            profile_info = parts[2].strip()
            proxyIP, proxyPort, proxyUsername, proxyPassword = proxy_info.split(':')
            profile_id, serial_number = profile_info.split(':')
            extracted_data.append((cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number))
    
    return extracted_data

def format_full_name(full_name):
    name_parts = full_name.replace('.', '').strip().lower().split()
    
    if len(name_parts) > 0:
        first_name = name_parts[0]
        last_name = name_parts[-1]
        return first_name, last_name
    return '', ''

def generate_email_from_full_name(full_name):
    first_name, last_name = format_full_name(full_name)
    cleaned_first_name = first_name.replace(' ', '').lower()
    cleaned_last_name = last_name.replace(' ', '').lower()
    fullName = cleaned_first_name + cleaned_last_name
    domains = ['outlook.com', 'gmail.com', 'hotmail.com']
    random_domain = random.choice(domains)
    random_numbers = random.randint(1, 9999)
    return f"{fullName}{random_numbers}@{random_domain}"

def randomize_case(text):
    return ''.join(
        char.upper() if random.choice([True, False]) else char.lower() 
        for char in text
    )

def generate_password_from_full_name(full_name):
    cleaned_name = full_name.replace(' ', '')
    randomized_full_name = randomize_case(cleaned_name)
    
    random_numbers = ''.join(random.choices(string.digits, k=4))
    
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    
    special_characters = '!@#$%^&*'
    
    random_specials = ''.join(
        random.choice(special_characters + string.digits)
        for _ in range(random.randint(1, 4))
    )
    
    return f"{randomized_full_name}{random_numbers}{random_part}{random_specials}"

def save_to_credentials(cpf):
    if os.path.exists(credentials_path):
        with open(credentials_path, 'r', encoding='utf-8') as file:
            existing_accounts = file.readlines()
            existing_accounts = [line.strip() for line in existing_accounts if line.strip()]

    updated_accounts = set(existing_accounts)
    updated_accounts.add(cpf)

    if updated_accounts:
        with open(credentials_path, 'w', encoding='utf-8') as file:
            file_content = '\n'.join(updated_accounts)
            file.write(file_content)

def save_proxies(proxyIP, proxyPort, proxyUsername, proxyPassword):
    proxy_line = f"{proxyIP}:{proxyPort}:{proxyUsername}:{proxyPassword}"

    existing_proxies = set()
    if os.path.exists(proxys_path):
        with open(proxys_path, 'r', encoding='utf-8') as file:
            existing_proxies = {line.strip() for line in file if line.strip()}

    if proxy_line and proxy_line not in existing_proxies:
        existing_proxies.add(proxy_line)

        with open(proxys_path, 'w', encoding='utf-8') as file:
            file_content = '\n'.join(sorted(existing_proxies))
            file.write(file_content)

def remove_account_line(cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number):
    account_line_to_remove = f"{cpf} - {proxyIP}:{proxyPort}:{proxyUsername}:{proxyPassword} - {profile_id}:{serial_number}"
    
    with open(credentials_2_path, 'r', encoding='utf-8') as file:
        accounts = file.readlines()
    
    updated_accounts = [account.strip() for account in accounts if account.strip() != account_line_to_remove]

    if len(updated_accounts) < len(accounts):
        with open(credentials_2_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(updated_accounts) + '\n' if updated_accounts else '')
    
def save_account(email, password, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number):
    existing_accounts = []
    
    if os.path.exists(profiles_create_path):
        with open(profiles_create_path, 'r', encoding='utf-8') as file:
            existing_accounts = file.readlines()
            existing_accounts = [line.strip() for line in existing_accounts if line.strip()]

    account_line = f"{email}:{password}:{cpf} - {proxyIP}:{proxyPort}:{proxyUsername}:{proxyPassword} - {profile_id}:{serial_number}"

    updated_accounts = set(existing_accounts)

    if account_line.strip() not in updated_accounts:
        updated_accounts.add(account_line.strip())

        with open(profiles_create_path, 'w', encoding='utf-8') as file:
            file_content = '\n'.join(updated_accounts)
            file.write(file_content)

def pull_full_name(cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number):
    try:

        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--incognito")
        driver = uc.Chrome(options=options)
        print(f"{yellow}[INFO]{reset} {purple}Conectado na API com sucesso!{reset}", end='')
        sys.stdout.flush()

        time.sleep(0.200)

        driver.get('https://lotogreen.com/')

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__nuxt"]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/button[4]'))
        )
        button.click()

        cpf_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__nuxt"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/form/div[3]/div/div[1]'))
        )
        cpf_field = cpf_container.find_element(By.XPATH, './input')
        cpf_field.send_keys(cpf)

        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="relative flex-1"]/input[@name="username" and @placeholder="Nome"]'))
        )

        full_name = input_element.get_attribute('data-maska-value')

        if not full_name.strip():
            print(f"{red}[ERROR]{reset} {purple}Nome completo não encontrado, tente novamente!{reset}")
            save_to_credentials(cpf)
            save_proxies(proxyIP, proxyPort, proxyUsername, proxyPassword)
            delete_profile(profile_id, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, serial_number)
            return
        else:
            print(f"{yellow}[INFO]{reset} {purple}Nome completo encontrado: {full_name}{reset}")
        first_name, last_name = format_full_name(full_name)
        email = generate_email_from_full_name(f"{first_name} {last_name}")
        password = generate_password_from_full_name(f"{first_name} {last_name}")

        save_account(email, password, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number)
        remove_account_line(cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number)
        print(f"{green}[SUCCESS 2/2]{reset} {purple}({cpf}) - Informações Coletadas com sucesso! {full_name} - {email} - {password}{reset}", end='')
        sys.stdout.flush()

    except Exception as error:
        print(f"{red}[ERROR]{reset} {purple}({cpf}) - Ocorreu um erro interno, contate aos administradores.{reset}\n{error}", end='')
        sys.stdout.flush()
        delete_profile(profile_id, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, serial_number)
        save_to_credentials(cpf)
        save_proxies(proxyIP, proxyPort, proxyUsername, proxyPassword)

def check_browser_status(profile_id, cpf):
    url = f"{config['AdsPower']['urlLocal']}/api/v1/browser/active"
    params = {"user_id": profile_id}

    while True:
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data["code"] == 0:
                if data["data"]["status"] == "Inactive":
                    break
            else:
                print(f"{red}[ERROR]{reset} {purple}({cpf}) - Falha ao verificar o status do navegador.{reset}", end='')
                sys.stdout.flush()
                break
        except Exception as error:
            print(f"{red}[ERROR]{reset} {purple}({cpf}) - Erro ao verificar o status do navegador.{reset}", end='')
            sys.stdout.flush()
            break

        time.sleep(1)

def delete_profile(profile_id, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, serial_number):
    check_browser_status(profile_id, cpf)
    time.sleep(1)

    url = f"{config['AdsPower']['urlLocal']}/api/v1/user/delete"
    params = {"user_ids": [profile_id]}

    try:
        response = requests.post(url, json=params)
        data = response.json()
        if data["code"] == 0:
            remove_account_line(cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number)
        elif "is being used by" in data.get("msg", ""):
            pass
        else:
            pass
    except Exception as error:
        print(f"{red}[ERROR]{reset} {purple}({cpf}) - Erro ao tentar deletar perfil.{reset}")
        sys.stdout.flush()

if __name__ == "__main__":
    verificar_max_user()
    accounts = get_accounts()
    for account in accounts:
        cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number = account
        pull_full_name(cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id, serial_number)