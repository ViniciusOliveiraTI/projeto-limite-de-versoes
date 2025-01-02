const filterByDate = document.getElementById('filterByDate');
const filterFolders = document.getElementById('filterFolders');
const dateInput = document.getElementById('date');
const versionInput = document.getElementById('versoes');
const folderInput = document.getElementById('select-folder');
const form = document.getElementById('form');
const submitMain = document.getElementById('submit-main');
const confirmSubmissionButton = document.getElementById('confirmSubmission');


// Controlar habilitação dos campos de data e versão
filterByDate.addEventListener('change', () => {
    if (filterByDate.checked) {
        dateInput.disabled = false;
        versionInput.disabled = true;
    } else {
        dateInput.disabled = true;
        versionInput.disabled = false;
    }
});

// Controlar habilitação do campo de pastas
filterFolders.addEventListener('change', () => {
    if (filterFolders.checked) {
        folderInput.disabled = false;
    } else {
        folderInput.disabled = true;
    }
});

 // Abrir modal de confirmação ao clicar no botão principal
submitMain.addEventListener('click', (event) => {
    event.preventDefault(); // Evita o envio automático do formulário
    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    confirmationModal.show();
});

// Confirmar envio no modal
confirmSubmissionButton.addEventListener('click', () => {
    const confirmationModal = bootstrap.Modal.getInstance(document.getElementById('confirmationModal'));
    confirmationModal.hide(); // Fecha o modal
    form.submit(); // Submete o formulário
});