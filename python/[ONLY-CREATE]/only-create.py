import argparse
import requests
import time
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import sys
import io
import threading

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

blue = Fore.BLUE
green = Fore.GREEN
yellow = Fore.YELLOW
red = Fore.RED
roxo = Fore.MAGENTA
reset = Fore.RESET

config_path = './config.json'
if not os.path.exists(config_path):
    print(f"{red}[ERROR]{reset} {roxo}O arquivo de configuração não foi encontrado.{reset}", end='')
    sys.stdout.flush()
    sys.exit(1)

with open(config_path) as config_file:
    config = json.load(config_file)

profiles_create_path = './[UNKOYNX7]/[ONLY-CREATE]/profilesCreate.txt'
accountCreatePath = './[UNKOYNX7]/[ONLY-CREATE]/accountCreate.txt'
proxiesUsedPath = './[UNKOYNX7]/[ONLY-CREATE]/proxiesUsed.txt'

def get_accounts():
    if not os.path.exists(profiles_create_path):
        print(f"{red}[ERROR]{reset} {roxo}O arquivo de perfils criados não foi encontrado.{reset}", end='')
        sys.stdout.flush()
        sys.exit(1)

    with open(profiles_create_path, 'r', encoding='utf-8') as file:
        accounts = file.readlines()
    
    accounts = [line.strip() for line in accounts if line.strip()]
    
    if not accounts:
        print(f"{red}[ERROR]{reset} {roxo}Nenhuma conta disponível.{reset}")
        sys.stdout.flush()
        sys.stdout.flush()
        return []

    return accounts

def remove_account_line(account_line):
    with open(profiles_create_path, 'r', encoding='utf-8') as file:
        accounts = file.readlines()
    updated_accounts = [account.strip() for account in accounts if account.strip() and account.strip() != account_line]
    with open(profiles_create_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(updated_accounts) + '\n' if updated_accounts else '')

    sys.stdout.flush()

def click_button_when_clickable(driver, cpf, xpath):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()
        print(f"{yellow}[INFO]{reset} {roxo}({cpf}) - Botão clicado com sucesso!{reset}", end='')
        sys.stdout.flush()
    except Exception as e:
        print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Erro ao tentar clicar no botão.{reset}", end='')
        sys.stdout.flush()

def type_with_delay(element, text, delay=100):
    element.click()
    for char in text:
        element.send_keys(char)
        time.sleep(delay / 1000.0)

def fill_form_and_submit(driver, account_data, email, password, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id):
    try:
        email_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="auth-modal"]/div[2]/form/div[1]/div'))
        )
        email_field = email_container.find_element(By.XPATH, './input')
        email_field.send_keys(email)
        
        senha_container = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="auth-modal"]/div[2]/form/div[2]/div'))
        )
        senha_field = senha_container.find_element(By.XPATH, './input')
        senha_field.send_keys(password)

        cpf_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="auth-modal"]/div[2]/form/div[3]/div/div/div/div/input'))
        )
        type_with_delay(cpf_field, cpf, delay=100)

        try:
            error_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.error-label"))
            )
            error_message = error_element.text
            if ("Este CPF pertence a um menor e não pode ser aceito" in error_message or
                "O CPF fornecido é inválido. Insira um número de CPF válido." in error_message):
                print(f"{red}[ERROR]{reset} {roxo}({cpf}) - {error_message}{reset}")
                delete_profile(profile_id, account_data, proxyIP, proxyPort, proxyUsername, proxyPassword, cpf)
                return
        except Exception:
            pass

        click_button_when_clickable(driver, cpf, '//*[@id="auth-modal"]/div[2]/form/div[5]/button')

        try:
            cpf_error_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="auth-modal"]/div[2]/form/div[3]/div/div/div/div[2]'))
            )
            if cpf_error_element.is_displayed():
                print(f"{red}[ERROR]{reset} {roxo}({cpf}) - O cpf já está cadastrado.{reset}")
                delete_profile(profile_id, account_data, proxyIP, proxyPort, proxyUsername, proxyPassword, cpf)
                return
        except Exception:
            pass

        try:
            email_error_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="auth-modal"]/div[2]/form/div[2]'))
            )
            if email_error_element:
                print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Já existe uma conta com esse e-mail.{reset}")
                delete_profile(profile_id, account_data, proxyIP, proxyPort, proxyUsername, proxyPassword, cpf)
                return
        except Exception:
            pass

        try:
            success_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="welcome-header" and text()="Bem-vindo ao Jonbet!"]'))
            )
            if success_message:
                print(f"{green}[SUCCESS]{reset} {roxo}({cpf}) - Conta criada com sucesso!{reset}", end='')
                sys.stdout.flush()
                save_proxies(proxyIP, proxyPort, proxyUsername, proxyPassword)
                save_account(email, password, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword)
                delete_profile(profile_id, account_data, proxyIP, proxyPort, proxyUsername, proxyPassword, cpf)
        except Exception:
            print(f"{green}[SUCCESS]{reset} {roxo}({cpf}) - Conta foi criada, mas a verificação não foi encontrada.{reset}", end='')
            sys.stdout.flush()
    except Exception as e:
        print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Erro ao criar a conta.{reset}", end='')
        sys.stdout.flush()

def check_if_content_is_visible(driver):
    try:
        content_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="policy-regulation-popup"]/div/div[2]/div/button'))
        )
        return True
    except Exception:
        return False
    
def save_account(email, password, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword):
    account_line = f"{email}:{password}:{cpf} - {proxyIP}:{proxyPort}:{proxyUsername}:{proxyPassword}\n"

    with open(accountCreatePath, 'a', encoding='utf-8') as file:
        file.write(account_line)

def save_proxies(proxyIP, proxyPort, proxyUsername, proxyPassword):
    proxy_line = f"{proxyIP}:{proxyPort}:{proxyUsername}:{proxyPassword}"

    existing_proxies = set()
    if os.path.exists(proxiesUsedPath):
        with open(proxiesUsedPath, 'r', encoding='utf-8') as file:
            existing_proxies = {line.strip() for line in file if line.strip()}

    if proxy_line and proxy_line not in existing_proxies:
        existing_proxies.add(proxy_line)

        with open(proxiesUsedPath, 'w', encoding='utf-8') as file:
            file_content = '\n'.join(sorted(existing_proxies))
            file.write(file_content)

def create_account(account_data):
    if not account_data or not isinstance(account_data, str):
        print(f"{red}[ERROR]{reset} {roxo}Dados da conta não são válidos.{reset}", end='')
        sys.stdout.flush()
        return

    credentials, proxy, additional_info = account_data.split(' - ')
    email, password, cpf = credentials.split(':')
    proxyIP, proxyPort, proxyUsername, proxyPassword = proxy.split(':')
    profile_id = additional_info.split(':')[0].strip()

    open_url = f"{config['AdsPower']['urlLocal']}/api/v1/browser/start?user_id={profile_id}"

    resp = requests.get(open_url).json()

    if resp["code"] != 0:
        print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Perfil no adsPower não existe.{reset}", end='')
        sys.stdout.flush()
        return

    chrome_driver = resp["data"]["webdriver"]
    debugger_address = resp["data"]["ws"]["selenium"]

    if ':' not in debugger_address:
        print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Ocorreu um erro no debuggerAddress, contate aos administradores!'.{reset}", end='')
        sys.stdout.flush()
        return
    else:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", debugger_address)

    driver = None

    try:
        driver = webdriver.Chrome(service=Service(chrome_driver), options=chrome_options)
        print(f"{green}[SUCCESS]{reset} {roxo}({cpf}) - Conectado ao navegador com sucesso!{reset}", end='')
        sys.stdout.flush()

        time.sleep(2)

        driver.get(f"{config['AdsPower']['linkJonbet']}")
        print(f"{yellow}[INFO]{reset} {roxo}({cpf}) - Link aberto com sucesso!{reset}", end='')
        sys.stdout.flush()

        if check_if_content_is_visible(driver):
            click_button_when_clickable(driver, cpf, '//*[@id="policy-regulation-popup"]/div/div[2]/div/button')
        else:
            print(f"{yellow}[INFO]{reset} {roxo}({cpf}) - Botão de cookies já aceito.{reset}", end='')
            sys.stdout.flush()

        click_button_when_clickable(driver, cpf, '//*[@id="landing-home"]/div[1]/div/div/div[1]/div[2]/div/button')

        fill_form_and_submit(driver, account_data, email, password, cpf, proxyIP, proxyPort, proxyUsername, proxyPassword, profile_id)

    except Exception as error:
        print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Ocorreu um erro conectar ao selenium.{reset}", end='')
        sys.stdout.flush()
    finally:
        if driver:
            driver.quit()

def close_browser(profile_id):
    close_url = f"{config['AdsPower']['urlLocal']}/api/v1/browser/stop?user_id={profile_id}"
    requests.get(close_url)

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
                print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Falha ao verificar o status do navegador.{reset}", end='')
                sys.stdout.flush()
                break
        except Exception as error:
            print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Erro ao verificar o status do navegador.{reset}", end='')
            sys.stdout.flush()
            break

        time.sleep(1)

def delete_profile(profile_id, account_data, proxyIP, proxyPort, proxyUsername, proxyPassword, cpf):
    close_browser(profile_id)
    check_browser_status(profile_id, cpf)
    save_proxies(proxyIP, proxyPort, proxyUsername, proxyPassword)
    time.sleep(1)

    url = f"{config['AdsPower']['urlLocal']}/api/v1/user/delete"
    params = {"user_ids": [profile_id]}

    try:
        response = requests.post(url, json=params)
        data = response.json()
        if data["code"] == 0:
            remove_account_line(account_data)
        elif "is being used by" in data.get("msg", ""):
            pass
        else:
            pass
    except Exception as error:
        print(f"{red}[ERROR]{reset} {roxo}({cpf}) - Erro ao tentar deletar perfil.{reset}")
        sys.stdout.flush()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script para criar contas com múltiplos navegadores.')
    parser.add_argument('--max_browsers', type=int, required=True, help='Número máximo de navegadores a serem usados.')
    return parser.parse_args()

def main():
    args = parse_arguments()
    accounts = get_accounts()
    
    threads = []
    max_browsers = min(args.max_browsers, len(accounts))

    for i, account in enumerate(accounts[:max_browsers]):
        if i > 0:
            time.sleep(0.500)

        thread = threading.Thread(target=create_account, args=(account,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()