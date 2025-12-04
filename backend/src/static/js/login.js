document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('login-form');
    const msgDiv = document.getElementById('mensagem');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        msgDiv.innerText = "";
        const btn = loginForm.querySelector('button');
        const textoOriginal = btn.innerText;
        btn.innerText = "Entrando";
        btn.disabled = true;

        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        try {

            const response = await fetch('http://127.0.0.1:5000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    Email: email,
                    Senha: senha
                })

            });

            const data = await response.json();

            if (response.ok) {

                msgDiv.style.color = "#4cd137";
                msgDiv.innerText = "Login realizado! Redirecionando";

                localStorage.setItem('token', data.token);
                localStorage.setItem('user_id', data.user_id);

                setTimeout(() => {
                    window.location.href = '/'; //depois mudar para dashboard aqui
                }, 1000);

            } 
            else{

                msgDiv.style.color = "#ff6b6b";
                msgDiv.innerText = data.mensagem || "Erro ao fazer login.";

                btn.innerText = textoOriginal;
                btn.disabled = false;
            }

        } catch (error) {
            console.error(error);
            msgDiv.style.color = "#ff6b6b";
            msgDiv.innerText = "Erro de conexão com o servidor.";

            btn.innerText = textoOriginal;
            btn.disabled = false;
        }
    });
});