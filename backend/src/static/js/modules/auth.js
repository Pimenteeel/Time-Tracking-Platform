// Responsável apenas por saber quem é o usuário e se ele está logado
export function getToken() {
    return localStorage.getItem('token');
}

export function getUserId() {
    return localStorage.getItem('user_id');
}

export function verificarAutenticacao() {
    const token = getToken();
    if (!token) {
        window.location.href = '/login-page';
        return false;
    }
    return true;
}

export function logout() {
    localStorage.clear();
    window.location.href = '/login-page';
}