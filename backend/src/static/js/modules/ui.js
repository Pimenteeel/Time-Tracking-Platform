// Responsável por manipular o DOM visualmente (Cronômetro, planilhas, gestão)

export function setupNavigation() {
    const links = {
        'nav-cronometro': 'cronometro-view',
        'nav-planilha': 'planilha-view',
        'nav-gestao': 'gestao-view',
        'nav-relatorio-detalhado': 'relatorio-detalhado-view',
        'nav-relatorio-resumido': 'relatorio-detalhado-view',
        'nav-equipe-detalhado': 'gestao-view',
        'nav-equipe-resumido': 'gestao-view'
    };

    for (const [linkId, viewId] of Object.entries(links)) {
        const link = document.getElementById(linkId);

        if (link) {
            link.addEventListener('click', (e) => {
                e.preventDefault();

                document.querySelectorAll('.view').forEach(el => el.computedStyleMap.display = 'none');

                document.querySelectorAll('.sidebar-nav a').forEach(el => el.classList.remove('active'));

                const view = document.getElementById(viewId);
                if (view) {
                    view.style.display = 'block';
                    link.classList.add('active');
                }
            });
        }
    }
}

export function preencherSelect(selectId, dados, placeholder = "Selecione...") {
    const select = document.getElementById(selectId);
    if (!select) return;

    select.innerHTML = `<option value="" disabled selected>${placeholder}</option>`;
    select.disabled = false;

    dados.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.innerText = item.nome;
        select.appendChild(option);
    });
}

export function setSelectLoading(selectId, loading = true) {
    const select = document.getElementById(selectId);
    if (!select) return;

    if (loading) {
        select.innerHTML = '<option disabled>Carregando...</option>';
        select.disabled = true;
    } else {
        select.disabled = false;
    }
}
