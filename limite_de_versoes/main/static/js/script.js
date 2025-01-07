document.addEventListener('DOMContentLoaded', () => {

    // Selecionando os elementos do DOM
    const filterByDate = document.getElementById('filterByDate');
    const filterFolders = document.getElementById('filterFolders');
    const dateInput = document.getElementById('date');
    const versionInput = document.getElementById('versoes');
    const folderInput = document.getElementById('select-folder');
    const siteInput = document.getElementById('select-site');
    const form = document.getElementById('form');
    const submitMain = document.getElementById('submit-main');
    const confirmSubmissionButton = document.getElementById('confirmSubmission');
    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));

    // Habilitar/Desabilitar os campos de data e versão
    if (filterByDate) {
        filterByDate.addEventListener('change', () => {
            dateInput.disabled = !filterByDate.checked;
            versionInput.disabled = filterByDate.checked;
        });
    }

    // Habilitar/Desabilitar o campo de pastas
    if (filterFolders) {
        filterFolders.addEventListener('change', () => {
            folderInput.disabled = !filterFolders.checked;
        });
    }

    // Abrir o modal de confirmação
    if (submitMain) {
        submitMain.addEventListener('click', (event) => {
            event.preventDefault();
            confirmationModal.show();
        });
    }

    // Confirmar envio no modal
    if (confirmSubmissionButton) {
        confirmSubmissionButton.addEventListener('click', () => {
            confirmationModal.hide();
            form.submit();
        });
    }

    // Carregar pastas ao mudar o site
    if (siteInput) {
        siteInput.addEventListener('change', () => {
            const siteId = siteInput.value;
            if (siteId) {
                fetch(`/get_folders/${siteId}/`)  // URL do Django para pegar pastas do site selecionado
                    .then(response => response.json())
                    .then(data => {
                        if (data.folders) {
                            // Resetar o campo de pastas
                            folderInput.innerHTML = '<option selected disabled>Selecione as pastas</option>';
                            data.folders.forEach(folder => {
                                const option = document.createElement('option');
                                option.value = folder.id;
                                option.textContent = folder.name;
                                folderInput.appendChild(option);
                            });
                            folderInput.disabled = false; // Habilitar o campo de pastas
                        }
                    })
                    .catch(error => {
                        console.error('Erro ao carregar as pastas:', error);
                    });
            } else {
                // Se nenhum site for selecionado, desabilitar o campo de pastas
                folderInput.innerHTML = '<option selected disabled>Selecione as pastas</option>';
                folderInput.disabled = true;
            }
        });
    }

});
