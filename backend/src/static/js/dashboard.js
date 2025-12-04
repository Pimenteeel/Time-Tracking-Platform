import * as Auth from './modules/auth.js';
import * as Api from './modules/api.js';
import * as UI from './modules/ui.js';
import * as Timer from './modules/timer.js';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Verifica Segurança
    if (!Auth.verificarAutenticacao()) return;

    // 2. Configura Logout
    document.getElementById('logout-btn').addEventListener('click', Auth.logout);

    // 3. Configura Navegação (Abas)
    UI.setupNavigation();

    // 4. Inicializa Lógica do Cronômetro
    Timer.initTimer();

    // 5. Carrega Dados Iniciais (Pilares)
    carregarDadosIniciais();
});

async function carregarDadosIniciais() {
    try {
        UI.setSelectLoading('pilar', true);
        const pilares = await Api.getPilares();
        UI.preencherSelect('pilar', pilares, "Selecione o Pilar");
        
        // Configura evento de mudança do Pilar
        document.getElementById('pilar').addEventListener('change', async (e) => {
            const pilarId = e.target.value;
            await carregarProjetosDoPilar(pilarId);
        });

    } catch (erro) {
        console.error(erro);
        alert("Erro ao carregar dados iniciais.");
    }
}

async function carregarProjetosDoPilar(pilarId) {
    try {
        UI.setSelectLoading('projeto', true);
        const projetos = await Api.getProjetos(pilarId);
        UI.preencherSelect('projeto', projetos, "Selecione o Projeto");
    } catch (erro) {
        console.error(erro);
        alert("Erro ao carregar projetos.");
    }
}