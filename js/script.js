document.addEventListener("DOMContentLoaded", function () {
    console.log("Sistema da Escola Benedito Oliveira inicializado com sucesso!");

    // ==========================================================================
// 1. TELA DE LOGIN: ALTERNAR PERFIL E OLHO DA SENHA
// ==========================================================================
try {
    const profileButtons = document.querySelectorAll(".profile-selector-box .profile-btn");
    const inputHiddenPerfil = document.getElementById("perfil_selecionado");

    if (profileButtons.length > 0) {
        profileButtons.forEach(btn => {
            btn.addEventListener("click", function() {
                profileButtons.forEach(b => b.classList.remove("active"));
                this.classList.add("active");
                
                // Pega o valor do botão clicado (diretor, responsavel, etc) e joga no input hidden
                const perfilValue = this.getAttribute("data-perfil");
                if (inputHiddenPerfil) {
                    inputHiddenPerfil.value = perfilValue;
                    console.log("Perfil selecionado para envio:", perfilValue);
                }
            });
        });
    }
} catch (e) { console.log("Abas de login não encontradas."); }

    // ==========================================================================
    // 2. DASHBOARD: BOTÕES SUPERIORES DE CANTO (HAMBÚRGUER E NOTIFICAÇÃO)
    // ==========================================================================
    try {
        // Mapeia os botões diretamente pelas classes exatas do seu HTML
        const menuTopBtn = document.querySelector(".menu-top-btn");
        const notchTopBtn = document.querySelector(".notification-top-btn");

        if (menuTopBtn) {
            menuTopBtn.addEventListener("click", function(e) {
                e.preventDefault();
                window.location.href = "/mais";
            });
        }

        if (notchTopBtn) {
            notchTopBtn.addEventListener("click", function(e) {
                e.preventDefault();
                window.location.href = "/notificacoes";
            });
        }
    } catch (e) { console.log("Botões superiores do topo não encontrados."); }

    // ==========================================================================
    // 3. TELA DE COMUNICADOS: FILTRO DINÂMICO POR ABAS
    // ==========================================================================
    try {
        const tabButtons = document.querySelectorAll(".sub-tabs .tab-btn");
        const comunicadoCards = document.querySelectorAll(".comunicados-list .comunicado-card");

        if (tabButtons.length > 0 && comunicadoCards.length > 0) {
            tabButtons.forEach(tab => {
                tab.addEventListener("click", function() {
                    const parentContainer = this.parentElement;
                    parentContainer.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
                    this.classList.add("active");
                    
                    const categoriaSelecionada = this.textContent.trim();
                    
                    comunicadoCards.forEach(card => {
                        const categoriaCard = card.getAttribute("data-categoria");
                        if (categoriaSelecionada === "Todas" || categoriaCard === categoriaSelecionada) {
                            card.style.display = "flex";
                        } else {
                            card.style.display = "none";
                        }
                    });
                });
            });
        }
    } catch (e) { console.log("Abas de comunicados não encontradas."); }
});