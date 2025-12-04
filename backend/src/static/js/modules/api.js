// Responsável por conversar com o python (backend)
import { getToken } from "./auth.js";

const BASE_URL = '/api';

async function request(endpoint, option = {}) {
    const token = getToken();

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.erro || 'Erro na comunicação com o servidor');
    }

    return data;
}

export async function getPilares() {
    return request('/pilares');
}

export async function getProjetos(pilarId) {
    return request(`/projetos/${pilarId}`);
}

export async function salvarApontamento(payload) {
    return request('/salvar', {
        method: 'POST',
        body: JSON.stringify(payload)
    });
}