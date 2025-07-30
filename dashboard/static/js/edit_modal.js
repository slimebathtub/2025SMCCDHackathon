document.addEventListener('DOMContentLoaded', function () {
    const editModal = document.getElementById('editModal');
    if (editModal) {
        editModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const url = button?.getAttribute('data-url');
            if (!url) return;
            console.log("Loading modal from URL:", url);
            const modalBody = document.getElementById('editModalBody');
            modalBody.innerHTML = '<p>Loading...</p>';
            fetch(url)
                .then(response => response.text())
                .then(html => modalBody.innerHTML = html)
                .catch(() => modalBody.innerHTML = '<p class="text-danger">Failed to load form.</p>');
        });
    }
});