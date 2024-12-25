import readline from 'readline';
import chalk from 'chalk';
import { spawn } from 'child_process';
import createUserProfiles from './functions/createUserProfile.js';
import createUserDeposit from './functions/createUserDeposit.js';
import listGroups from './functions/listGroups.js';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import path from 'path';

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const mainMenu = () => {
    console.clear();
    console.log(chalk.blue.bold("=== MENU CRIAR CONTA - DEPOSITO ==="));
    console.log(chalk.magenta("( 1 ) - Criar Perfil [ADS]( CONTA - DEPOSITO )"));
    console.log(chalk.green("( 2 ) - criar conta [ADS]( CONTA - DEPOSITO )"));

    console.log(chalk.blue.bold("\n=== MENU CRIAR CONTA + DEPOSITO ==="));
    console.log(chalk.magenta("( 3 ) - Criar perfil [ADS]( CONTA + DEPOSITO )"));
    console.log(chalk.green("( 4 ) - Criar conta [JONBET]( CONTA + DEPOSITO )"));

    console.log(chalk.blue.bold("\n=== MENU OUTROS ==="));
    console.log(chalk.green("( 5 ) - Listar grupos ( ADS )"));
    console.log(chalk.red("( 0 ) - Sair"));

    rl.question(chalk.cyan("\n$ "), (answer) => {
        switch (answer) {
            case '1':
                init().then(() => {
                    pauseAndReturnToMenu();
                }).catch(() => {
                    pauseAndReturnToMenu();
                });
                break;
            case '2':
                askForBrowserCount();
                break;
            case '3':
                init2().then(() => {
                    pauseAndReturnToMenu();
                }).catch(() => {
                    pauseAndReturnToMenu();
                });
                break;
            case '4':
                askForBrowserCount2();
                break;
            case '5':
                console.log(chalk.gray("\nExecutando a função de listagem de grupos..."));
                listGroups().then(() => {
                    pauseAndReturnToMenu();
                }).catch(() => {
                    pauseAndReturnToMenu();
                });
                break;
            case '0':
                console.log(chalk.red("\nSaindo..."));
                rl.close();
                break;
            default:
                console.log(chalk.red("\nOpção inválida."));
                pauseAndReturnToMenu();
        }
    });
};

const removeDuplicates = () => {
    console.log(chalk.gray("Executando a função de remover dados duplicados..."));
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ['./python/[ONLY-CREATE]/remove-duplicate.py']);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`${data.toString()}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`${data.toString()}`);
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error("Erro ao remover duplicados"));
            }
        });
    });
};

const removeDuplicates2 = () => {
    console.log(chalk.gray("Executando a função de remover dados duplicados..."));
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ['./python/[CREATE-DEPOSIT]/remove-duplicate.py']);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`${data.toString()}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`${data.toString()}`);
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error("Erro ao remover duplicados"));
            }
        });
    });
};

const genCredentials = () => {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ['./python/[ONLY-CREATE]/genCredentials.py']);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`${data.toString()}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`${data.toString()}`);
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error("Erro ao gerar credenciais"));
            }
        });
    });
};

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const init = async () => {
    try {
        const getCredentials = () => {
            const credentialsFilePath = path.join(__dirname, './[UNKOYNX7]/[ONLY-CREATE]/credentials.txt');
            const credentials = fs.readFileSync(credentialsFilePath, 'utf-8').split('\n').filter(Boolean);
            return credentials;
        };

        const getProxies = () => {
            const proxyFilePath = path.join(__dirname, './[UNKOYNX7]/[ONLY-CREATE]/proxys.txt');
            const proxies = fs.readFileSync(proxyFilePath, 'utf-8').split('\n').filter(Boolean);
            return proxies;
        };

        const proxies = getProxies();
        const credentials = getCredentials();
        const numProxies = proxies.length;
        const numCredentials = credentials.length;
        const maxProfiles = Math.min(numProxies, numCredentials);

        if (maxProfiles === 0) {
            console.log(chalk.red('[ERROR]'), chalk.magenta('Não há dados suficientes para criar perfis.'));
            return;
        }

        await removeDuplicates();
        console.log(chalk.gray('\nExecutando a função de criar perfil no adspower...'));
        await createUserProfiles();
        await genCredentials();
    } catch (error) {
        pauseAndReturnToMenu();
    }
};

const genCredentials2 = () => {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ['./python/[CREATE-DEPOSIT]/getCredentials.py']);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`${data.toString()}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`${data.toString()}`);
        });

        pythonProcess.on('close', (code) => {
            if (code === 0) {
                resolve();
            } else {
                reject(new Error("Erro ao gerar credenciais"));
            }
        });
    });
};

const init2 = async () => {
    try {
        const getCredentials = () => {
            const credentialsFilePath = path.join(__dirname, './[UNKOYNX7]/[CREATE-DEPOSIT]/credentials.txt');
            const credentials = fs.readFileSync(credentialsFilePath, 'utf-8').split('\n').filter(Boolean);
            return credentials;
        };

        const getProxies = () => {
            const proxyFilePath = path.join(__dirname, './[UNKOYNX7]/[CREATE-DEPOSIT]/proxys.txt');
            const proxies = fs.readFileSync(proxyFilePath, 'utf-8').split('\n').filter(Boolean);
            return proxies;
        };

        const proxies = getProxies();
        const credentials = getCredentials();
        const numProxies = proxies.length;
        const numCredentials = credentials.length;
        const maxProfiles = Math.min(numProxies, numCredentials);

        if (maxProfiles === 0) {
            console.log(chalk.red('[ERROR]'), chalk.magenta('Não há dados suficientes para criar perfis.'));
            return;
        }

        await removeDuplicates2();
        console.log(chalk.gray('\nExecutando a função de criar perfil no adspower...'));
        await createUserDeposit();
        await genCredentials2();
    } catch (error) {
        pauseAndReturnToMenu();
    }
};

const askForBrowserCount = () => {
    fs.readFile('./[UNKOYNX7]/[ONLY-CREATE]/profilesCreate.txt', 'utf8', (err, data) => {
        if (err) {
            console.error(chalk.red('Erro ao ler o arquivo de perfis:'), err);
            return;
        }

        const profiles = data.split('\n').filter(line => line.trim() !== '');
        const minBrowsers = 1;
        const maxBrowsers = profiles.length;

        if (maxBrowsers === 0) {
            console.log(chalk.red('[ERROR]', chalk.magenta(`Não há contas disponíveis, utilize a opção 1.`)));
            pauseAndReturnToMenu();
            return;
        }

        rl.question(chalk.cyan(`\nQuantos navegadores deseja utilizar? (Mínimo: ${minBrowsers}, Máximo: ${maxBrowsers}): `), (count) => {
            const browserCount = parseInt(count);

            if (isNaN(browserCount) || browserCount < minBrowsers || browserCount > maxBrowsers) {
                console.log(chalk.red(`\nPor favor, insira um número entre ${minBrowsers} e ${maxBrowsers}.`));
                askForBrowserCount();
            } else {
                console.log(chalk.gray(`\nExecutando a função de criar conta na jonbet com ${browserCount} navegador(es)...`));
                const pythonProcess = spawn('python', ['./python/[ONLY-CREATE]/only-create.py', '--max_browsers', browserCount]);

                pythonProcess.stdout.on('data', (data) => {
                    console.log(`${data.toString()}`);
                });

                pythonProcess.stderr.on('data', (data) => {
                    console.error(`${data.toString()}`);
                });

                pythonProcess.on('close', (code) => {
                    pauseAndReturnToMenu();
                });
            }
        });
    });
};

const askForBrowserCount2 = () => {
    fs.readFile('./[UNKOYNX7]/[CREATE-DEPOSIT]/profilesCreate.txt', 'utf8', (err, data) => {
        if (err) {
            console.error(chalk.red('Erro ao ler o arquivo de perfis:'), err);
            return;
        }

        const profiles = data.split('\n').filter(line => line.trim() !== '');
        const minBrowsers = 1;
        const maxBrowsers = profiles.length;

        if (maxBrowsers === 0) {
            console.log(chalk.red('[ERROR]', chalk.magenta(`Não há contas disponíveis, utilize a opção 3.`)));
            pauseAndReturnToMenu();
            return;
        }

        rl.question(chalk.cyan(`\nQuantos navegadores deseja utilizar? (Mínimo: ${minBrowsers}, Máximo: ${maxBrowsers}): `), (count) => {
            const browserCount = parseInt(count);

            if (isNaN(browserCount) || browserCount < minBrowsers || browserCount > maxBrowsers) {
                console.log(chalk.red(`\nPor favor, insira um número entre ${minBrowsers} e ${maxBrowsers}.`));
                askForBrowserCount();
            } else {
                console.log(chalk.gray(`\nExecutando a função de criar conta na jonbet com ${browserCount} navegador(es)...`));
                const pythonProcess = spawn('python', ['./python/[CREATE-DEPOSIT]/create-deposit.py', '--max_browsers', browserCount]);

                pythonProcess.stdout.on('data', (data) => {
                    console.log(`${data.toString()}`);
                });

                pythonProcess.stderr.on('data', (data) => {
                    console.error(`${data.toString()}`);
                });

                pythonProcess.on('close', (code) => {
                    pauseAndReturnToMenu();
                });
            }
        });
    });
};

const pauseAndReturnToMenu = () => {
    rl.question(chalk.blue(`\n[RETURN] Pressione ENTER para voltar...`), () => {
        mainMenu();
    });
};

mainMenu();