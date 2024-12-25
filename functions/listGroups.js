import axios from 'axios';
import fs from 'fs';
import path from 'path';
import config from "../config.json" assert { type: "json" };
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import chalk from 'chalk';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const apiUrlGroup = `${config.AdsPower.urlLocal}/api/v1/group/list`;
const apiKey = `${config.AdsPower.apiKey}`;

const listGroups = async () => {
    try {
        const response = await axios.get(apiUrlGroup, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json',
            }
        });

        const directory = path.join(__dirname, '../[UNKOYNX7]');
        const filePath = path.join(directory, 'groupId.txt');

        if (!fs.existsSync(directory)) {
            fs.mkdirSync(directory, { recursive: true });
        }

        fs.writeFileSync(filePath, JSON.stringify(response.data, null, 2));

        console.log(chalk.green(`[SUCCESS]`), chalk.magenta(`Foi um sucesso ao listar os grupos!`));

    } catch (error) {
        console.log(chalk.red(`[ERROR]`), chalk.magenta(`Ocorreu um erro ao listar os grupos, contato aos administradores!`));
    }
};

export default listGroups;