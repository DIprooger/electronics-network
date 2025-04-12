document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', function () {
            const emailId = this.dataset.id;
            const email = document.getElementById(`email-${emailId}`).textContent;

            navigator.clipboard.writeText(email).then(() => {
                alert("Email скопирован в буфер обмена!");
            }).catch(err => {
                alert("Ошибка копирования: " + err);
            });
        });
    });
});
