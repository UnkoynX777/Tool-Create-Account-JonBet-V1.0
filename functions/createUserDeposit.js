import axios from 'axios';
import config from "../config.json" assert { type: "json" };
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import fs from 'fs';
import path from 'path';
import promptSync from 'prompt-sync';
import chalk from 'chalk';

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const maxUserPath = path.join(__dirname, '../[UNKOYNX7]/maxUser.txt');

const apiUrlUserCreate = `${config.AdsPower.urlLocal}/api/v1/user/create`;
const apiKey = `${config.AdsPower.apiKey}`;

const prompt = promptSync();

const getProxies = () => {
    const proxyFilePath = path.join(__dirname, '../[UNKOYNX7]/[CREATE-DEPOSIT]/proxys.txt');
    const proxies = fs.readFileSync(proxyFilePath, 'utf-8').split('\n').filter(Boolean);
    return proxies;
};

const removeProxy = (proxy) => {
    const proxyFilePath = path.join(__dirname, '../[UNKOYNX7]/[CREATE-DEPOSIT]/proxys.txt');
    const proxies = fs.readFileSync(proxyFilePath, 'utf-8').split('\n').filter(Boolean);
    const updatedProxies = proxies.filter(p => p !== proxy);
    fs.writeFileSync(proxyFilePath, updatedProxies.join('\n'));
};

const getCredentials = () => {
    const credentialsFilePath = path.join(__dirname, '../[UNKOYNX7]/[CREATE-DEPOSIT]/credentials.txt');
    const credentials = fs.readFileSync(credentialsFilePath, 'utf-8').split('\n').filter(Boolean);
    return credentials;
};

const removeCredential = (credential) => {
    const credentialsFilePath = path.join(__dirname, '../[UNKOYNX7]/[CREATE-DEPOSIT]/credentials.txt');
    const credentials = fs.readFileSync(credentialsFilePath, 'utf-8').split('\n').filter(Boolean);
    const updatedCredentials = credentials.filter(c => c !== credential);
    fs.writeFileSync(credentialsFilePath, updatedCredentials.join('\n'));
};

const isValidCpf = (cpf) => {
    const cpfPattern = /^(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$/;
    return cpfPattern.test(cpf);
};

const saveProfileInfo = (credentialUsed, proxyUsed, profileId) => {
    const credentialsFilePath = path.join(__dirname, '../[UNKOYNX7]/[CREATE-DEPOSIT]/credentials-2.txt');
    const profileInfo = `${credentialUsed.trim()} - ${proxyUsed.trim()} - ${profileId.trim()}`;

    let fileContent = fs.existsSync(credentialsFilePath) ? fs.readFileSync(credentialsFilePath, 'utf-8').trimEnd() : '';

    const newContent = fileContent ? `${fileContent}\n${profileInfo}` : profileInfo;

    fs.writeFileSync(credentialsFilePath, newContent, 'utf-8');
};

const createUserDeposit = async () => {
    const proxies = getProxies();
    const credentials = getCredentials();

    const numProxies = proxies.length;
    const numCredentials = credentials.length;

    const maxProfiles = Math.min(numProxies, numCredentials);

    if (maxProfiles === 0) {
        console.log(chalk.red(`[ERROR]`), chalk.magenta(`Não há dados suficientes para criar perfis.`));
        return;
    }

    const input = prompt(chalk.yellow(`Quantos perfis você deseja gerar (máximo ${maxProfiles}): `));
    const requestedProfiles = parseInt(input, 10);

    if (isNaN(requestedProfiles) || requestedProfiles < 1 || requestedProfiles > maxProfiles) {
        console.error(chalk.red(`[ERROR]`), chalk.magenta(`Número inválido. Por favor, insira um número entre 1 e ${maxProfiles}.`));
        return;
    }

    for (let i = 0; i < requestedProfiles; i++) {
        const selectedCredential = credentials[i];
        const [cpf] = selectedCredential.split(':').map(item => item.trim());

        if (!isValidCpf(cpf)) {
            console.error(chalk.red(`[ERROR]`), chalk.magenta(`Formato de CPF inválido.`));
            continue;
        }

        const selectedProxy = proxies[i];
        const [proxyHost, proxyPort, proxyUser, proxyPassword] = selectedProxy.split(':').map(item => item.trim());

        const userProfileData = {
            name: cpf,
            open_urls: [`discord.gg/nexus-service`],
            group_id: config.AdsPower.groupId,
            user_proxy_config: {
                proxy_soft: config.AdsPower.proxy_soft,
                proxy_type: config.AdsPower.proxy_type,
                proxy_host: proxyHost,
                proxy_port: proxyPort,
                proxy_user: proxyUser,
                proxy_password: proxyPassword
            },
            fingerprint_config: {
                automatic_timezone: "1",
                webrtc: "disabled"
            }
        };

        if (!userProfileData.name || !userProfileData.open_urls.length || !userProfileData.group_id) {
            console.error(chalk.red(`[ERROR]`), chalk.magenta(`Dados do perfil incompletos.`));
            return;
        }

        const response = await axios.post(apiUrlUserCreate, userProfileData, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
            }
        });

        if (response.data && response.data.msg.includes('If the number of imported accounts exceeds the limit of 15')) {
            console.log(chalk.red('[ERROR]'), chalk.magenta(`(${cpf}) - Já existe o máximo de perfis criados!`));
            fs.writeFile(maxUserPath, 'true', (err) => {});
        } else {
            const responseData = response.data?.data;
            if (responseData) {
                const { id, serial_number } = responseData;
                const profileInfo = `${id}:${serial_number}`;
                saveProfileInfo(selectedCredential, selectedProxy, profileInfo);
                removeProxy(selectedProxy);
                removeCredential(selectedCredential);
                fs.writeFile(maxUserPath, 'false', (err) => {});
                console.log(chalk.green(`[SUCCESS 1/2]`), chalk.magenta(`(${cpf}) - Perfil criado no adspower com sucesso! - ${serial_number}`));
            } else {
                console.error(chalk.red(`[ERROR]`), chalk.magenta(`Ocorreu um erro interno na api, contate aos administradores.`));
            }
        }
        await delay(300);
    }
};

export default createUserDeposit;