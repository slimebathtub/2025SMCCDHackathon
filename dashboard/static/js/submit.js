document.addEventListener('submit', function (event) {
    const form = event.target;
    if (form.classList.contains('ajax-edit-form')) {
        event.preventDefault();

        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => {
            if (response.ok) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
                modal.hide();
                window.location.reload();
            } else {
                return response.text().then(html => {
                    document.getElementById('editModalBody').innerHTML = html;
                });
            }
        });
    }
});