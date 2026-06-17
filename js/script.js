document.addEventListener("DOMContentLoaded", function () {
    console.log("Sistema da Escola Benedito Oliveira inicializado com sucesso!");

    // ==========================================================================
    // 1. TELA DE LOGIN: ALTERNAR PERFIL E INPUT HIDDEN
    // ==========================================================================
    try {
        const profileButtons = document.querySelectorAll(".profile-selector-box .profile-btn");
        const inputHiddenPerfil = document.getElementById("perfil_selecionado");

        if (profileButtons.length > 0) {
            profileButtons.forEach(btn => {
                btn.addEventListener("click", function() {
                    profileButtons.forEach(b => b.classList.remove("active"));
                    this.classList.add("active");
                    
                    const perfilValue = this.getAttribute("data-perfil");
                    if (inputHiddenPerfil) {
                        inputHiddenPerfil.value = perfilValue;
                        console.log("Perfil selecionado para envio:", perfilValue);
                    }
                });
            });
        }
    } catch (e) { console.log("Erro nas abas de login:", e); }

    // ==========================================================================
    // 2. DASHBOARD: BOTÕES SUPERIORES DE CANTO (HAMBÚRGUER E NOTIFICAÇÃO)
    // ==========================================================================
    try {
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
    // 3. TELA DE COMUNICADOS: FILTRO DINÂMICO POR ABAS (VISÃO DO RESPONSÁVEL)
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


    // ==========================================================================
    // 4. ATUALIZAÇÃO EM TEMPO REAL COM LOADING (PAINEL DO DIRETOR)
    // ==========================================================================
    
    // Função para exibir o balão Push (Toast) corrigida
    function mostrarToast(mensagem) {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');
        if (toast && toastMessage) {
            toastMessage.innerText = mensagem;
            toast.className = "toast-notification show";
            setTimeout(function() {
                toast.className = toast.className.replace("show", "");
            }, 2500);
        }
    }

    // Função genérica para enviar formulários via AJAX com animação de Spinner
    function configurarFormularioAjax(idFormulario, rotaUrl, tipoForm) {
        const form = document.getElementById(idFormulario);
        if (!form) return; 

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const botaoSubmit = form.querySelector('button[type="submit"]');
            const textoOriginalBotao = botaoSubmit.innerHTML;
            
            // Ativa o efeito visual de carregamento no botão
            botaoSubmit.disabled = true;
            botaoSubmit.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Enviando...`;
            botaoSubmit.style.opacity = "0.7";

            const formData = new FormData(this);

            fetch(rotaUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Restaura o botão original após a resposta do servidor
                botaoSubmit.disabled = false;
                botaoSubmit.innerHTML = textoOriginalBotao;
                botaoSubmit.style.opacity = "1";

                if (data.status === 'sucesso') {
                    mostrarToast(data.mensagem);
                    
                    const idCriado = data.id || Date.now();
                    let novoItem = document.createElement('div');
                    
                    // Configuração inicial oculta para a animação de fade-in suave
                    novoItem.style = "display: flex; justify-content: space-between; align-items: center; background: #f9f9f9; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; font-size: 13px; border-left: 4px solid #b30000; opacity: 0; transform: translateY(-10px); transition: all 0.4s ease;";
                    
                    if (tipoForm === 'comunicado') {
                        const tipo = form.querySelector('[name="tipo"]').value;
                        const titulo = form.querySelector('[name="titulo"]').value;
                        
                        let badgeTexto = "Aviso Geral";
                        if (tipo === "Reuniões") badgeTexto = "Reunião de Pais";
                        if (tipo === "Avaliações") badgeTexto = "Avaliação / Prova";

                        novoItem.innerHTML = `
                            <span><strong>[${badgeTexto}]</strong> ${titulo}</span>
                            <a href="/deletar_comunicado/${idCriado}" style="background:transparent; border:none; color:red; cursor:pointer; text-decoration: none;">
                                <i class="fas fa-trash-alt"></i>
                            </a>
                        `;
                        // Insere no topo da lista (abaixo do h5)
                        const h5Alvo = form.parentElement.querySelector('h5');
                        if (h5Alvo) h5Alvo.insertAdjacentElement('afterend', novoItem);
                    } 
                    else if (tipoForm === 'evento') {
                        const dataInput = form.querySelector('[name="data"]').value;
                        const titulo = form.querySelector('[name="titulo"]').value;
                        const dataBr = dataInput.split('-').reverse().slice(0,2).join('/');

                        novoItem.innerHTML = `
                            <span><strong>${dataBr}</strong> - ${titulo}</span>
                            <a href="/deletar_evento/${idCriado}" style="background:transparent; border:none; color:red; cursor:pointer; text-decoration: none;">
                                <i class="fas fa-trash-alt"></i>
                            </a>
                        `;
                        form.parentElement.appendChild(novoItem);
                    } 
                    else if (tipoForm === 'prova') {
                        const disciplina = form.querySelector('[name="disciplina"]').value;
                        const conteudo = form.querySelector('[name="conteudo"]').value;
                        const dataInput = form.querySelector('[name="data"]').value;
                        const dataBr = dataInput.split('-').reverse().slice(0,2).join('/');

                        novoItem.innerHTML = `
                            <span><strong>${dataBr}</strong> - ${disciplina} (${conteudo})</span>
                            <a href="/deletar_prova/${idCriado}" style="background:transparent; border:none; color:red; cursor:pointer; text-decoration: none;">
                                <i class="fas fa-trash-alt"></i>
                            </a>
                        `;
                        form.parentElement.appendChild(novoItem);
                    }

                    // Força o navegador a processar os estilos e engatar a animação de entrada fluida
                    setTimeout(() => {
                        novoItem.style.opacity = "1";
                        novoItem.style.transform = "translateY(0)";
                    }, 50);

                    form.reset(); // Limpa as caixas do formulário
                }
            })
            .catch(error => {
                console.error('Erro no envio AJAX:', error);
                botaoSubmit.disabled = false;
                botaoSubmit.innerHTML = textoOriginalBotao;
                botaoSubmit.style.opacity = "1";
            });
        });
    }

    // Inicializa os formulários com proteção contra erros
    try {
        configurarFormularioAjax('form-comunicado', '/criar_comunicado', 'comunicado');
        configurarFormularioAjax('form-evento', '/criar_evento', 'evento');
        configurarFormularioAjax('form-prova', '/criar_prova', 'prova');
    } catch(err) { console.log("Formulários de gerenciamento não pertencem a esta página."); }

    // OUVINTE GLOBAL DAS LIXEIRAS (Para apagar na hora com efeito deslizante)
    document.addEventListener('click', function(e) {
        const botaoLixeira = e.target.closest('a[href*="/deletar_"]');
        
        if (botaoLixeira) {
            e.preventDefault(); 
            
            const urlDeletar = botaoLixeira.getAttribute('href');
            const containerItem = botaoLixeira.parentElement;

            fetch(urlDeletar)
            .then(() => {
                containerItem.style.transition = "all 0.25s ease";
                containerItem.style.opacity = "0";
                containerItem.style.transform = "translateX(15px)";
                
                setTimeout(() => {
                    containerItem.remove();
                    mostrarToast("Item removido com sucesso!");
                }, 250);
            })
            .catch(error => console.error('Erro ao deletar:', error));
        }
    });
});