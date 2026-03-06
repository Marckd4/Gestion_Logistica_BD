/**
 * Control de menús desplegables para la página de inicio
 */

// Control de menús desplegables
function toggleMenu(id) {
    event.stopPropagation();
    
    const menu = document.getElementById(id);
    const currentCard = menu.closest('.card-erp');
    const isVisible = menu.style.display === "block";

    // Cerrar todos los menús
    document.querySelectorAll('.erp-dropdown').forEach(el => {
        el.style.display = "none";
    });

    // Remover clase activa de todas las tarjetas
    document.querySelectorAll('.card-erp').forEach(card => {
        card.classList.remove('active-card');
    });

    // Alternar menú actual
    if (!isVisible) {
        menu.style.display = "block";
        currentCard.classList.add('active-card');
    }
}

// Cerrar menús al hacer clic fuera
document.addEventListener("click", function(event) {
    if (!event.target.closest(".card-erp")) {
        document.querySelectorAll('.erp-dropdown').forEach(el => {
            el.style.display = "none";
        });
        document.querySelectorAll('.card-erp').forEach(card => {
            card.classList.remove('active-card');
        });
    }
});

// Prevenir cierre al hacer clic en los links
document.querySelectorAll('.erp-dropdown a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});

// Notificación de clip
function mostrarClipInfo(id, modelo) {
    const toast = document.getElementById("clipToast");

    document.getElementById("clipId").innerText = id;
    document.getElementById("clipModelo").innerText = modelo;
    document.getElementById("clipFecha").innerText = new Date().toLocaleString('es-CL');

    toast.style.display = "block";

    setTimeout(() => {
        toast.style.display = "none";
    }, 5000);
}

// Efectos visuales - animación de tarjetas al cargar
window.addEventListener('load', () => {
    const cards = document.querySelectorAll('.card-erp');
    cards.forEach((card, index) => {
        card.style.animation = `fadeInUp 0.6s ease ${index * 0.1}s both`;
    });
});
