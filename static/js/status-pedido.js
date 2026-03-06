/**
 * Control de checkboxes en status de pedidos
 */
document.addEventListener('DOMContentLoaded', function () {
    const checkAll = document.getElementById('check-all');
    const checks = document.querySelectorAll('.nota-check');

    if (checkAll) {
        checkAll.addEventListener('change', function () {
            checks.forEach(c => c.checked = checkAll.checked);
        });
    }
});
