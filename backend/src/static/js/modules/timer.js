import * as Auth from './auth.js';
import * as Api from './api.js';

let intervalId = null;
let segundos = 0;
let isRunning = false;
let dataInicio = null;

// Elementos do DOM (Cache)
const display = document.getElementById('timer-display');
const btn = document.getElementById('btn-iniciar');
const inpPilar = document.getElementById('pilar');
const inpProjeto = document.getElementById('projeto');
const inpObs = document.getElementById('observacao');

export function initTimer() {
    // Adiciona o evento de click no botão Iniciar
    if (btn) {
        btn.addEventListener('click', toggleTimer);
    }
}

async function toggleTimer() {
    if (!isRunning) {
        iniciar();
    } else {
        await pararESalvar();
    }
}

function iniciar() {
    const projetoId = inpProjeto.value;
    
    if (!projetoId) {
        alert("⚠️ Selecione um PROJETO antes de iniciar.");
        return;
    }

    // Trava inputs
    inpPilar.disabled = true;
    inpProjeto.disabled = true;
    inpObs.disabled = true;

    // Estado inicial
    dataInicio = new Date();
    isRunning = true;
    
    // UI do Botão
    btn.innerText = "PARAR";
    btn.classList.add('parar');

    // Cronômetro Visual
    intervalId = setInterval(() => {
        segundos++;
        display.innerText = formatarTempo(segundos);
    }, 1000);
}

async function pararESalvar() {
    isRunning = false;
    clearInterval(intervalId);

    // UI de Carregamento
    btn.innerText = "SALVANDO...";
    btn.disabled = true;

    const dataFim = new Date();
    const payload = {
        user_id: Auth.getUserId(),
        projeto_id: inpProjeto.value,
        observacao: inpObs.value,
        inicio: dataInicio.toISOString(),
        fim: dataFim.toISOString()
    };

    try {
        const resposta = await Api.salvarApontamento(payload);
        alert(`✅ ${resposta.mensagem || 'Salvo com sucesso!'}`);
        resetar();
    } catch (erro) {
        console.error(erro);
        alert("Erro ao salvar: " + erro.message);
        
        // Se der erro, restaura o estado para permitir tentar de novo
        btn.innerText = "PARAR";
        btn.disabled = false;
        isRunning = true; // Volta a ficar rodando logicamente
    }
}

function resetar() {
    segundos = 0;
    dataInicio = null;
    display.innerText = "00:00:00";
    
    btn.innerText = "INICIAR";
    btn.classList.remove('parar');
    btn.disabled = false;

    // Destrava
    inpPilar.disabled = false;
    inpProjeto.disabled = true; // Projeto trava até selecionar pilar
    inpObs.disabled = false;

    // Limpa
    inpPilar.value = "";
    inpProjeto.innerHTML = '<option value="" disabled selected>Selecione um Pilar...</option>';
    inpObs.value = "";
}

function formatarTempo(segs) {
    const h = Math.floor(segs / 3600).toString().padStart(2, '0');
    const m = Math.floor((segs % 3600) / 60).toString().padStart(2, '0');
    const s = (segs % 60).toString().padStart(2, '0');
    return `${h}:${m}:${s}`;
}