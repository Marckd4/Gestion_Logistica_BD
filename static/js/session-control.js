/**
 * Control de sesión con advertencia de inactividad
 * Configuración: SESSION_TIMEOUT y WARNING_TIME en segundos
 */
document.addEventListener("DOMContentLoaded", function () {
    // Configuración de sesión (debe coincidir con SESSION_COOKIE_AGE en settings.py)
    const SESSION_TIMEOUT = 28800; // 8 horas en segundos
    const WARNING_TIME = 1500; // Mostrar advertencia 25 minutos antes (1500 segundos)
    
    let inactivityTimer = null;
    let warningShown = false;
    
    const resetInactivityTimer = () => {
        clearTimeout(inactivityTimer);
        warningShown = false;
        
        // Establecer temporizador para mostrar advertencia
        inactivityTimer = setTimeout(() => {
            if (!warningShown) {
                showInactivityWarning();
                warningShown = true;
            }
        }, (SESSION_TIMEOUT - WARNING_TIME) * 1000);
    };
    
    const showInactivityWarning = () => {
        // Crear modal de advertencia
        const warningHTML = `
            <div class="modal fade" id="inactivityWarning" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content border-warning">
                        <div class="modal-header bg-warning text-dark">
                            <h5 class="modal-title">⏰ Sesión por Expirar</h5>
                        </div>
                        <div class="modal-body">
                            <p>Tu sesión expirará en <strong id="countdown">25</strong> minutos por inactividad.</p>
                            <p>Haz clic en <strong>"Renovar Sesión"</strong> para continuar trabajando.</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-warning" id="renewSession">
                                🔄 Renovar Sesión
                            </button>
                            <a href="/logout/" class="btn btn-danger">
                                🚪 Cerrar Sesión
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al documento si no existe
        if (!document.getElementById('inactivityWarning')) {
            document.body.insertAdjacentHTML('beforeend', warningHTML);
        }
        
        // Mostrar modal con opciones (no cerrable con Escape ni al hacer clic afuera)
        const warningModal = document.getElementById('inactivityWarning');
        const modal = new bootstrap.Modal(warningModal, {
            backdrop: 'static',
            keyboard: false
        });
        modal.show();
        
        // Actualizar contador cada segundo
        let remainingTime = WARNING_TIME;
        const countdownInterval = setInterval(() => {
            remainingTime--;
            const minutes = Math.ceil(remainingTime / 60);
            const countdownEl = document.getElementById('countdown');
            if (countdownEl) {
                countdownEl.textContent = minutes;
            }
            
            if (remainingTime <= 0) {
                clearInterval(countdownInterval);
                modal.hide();
                // Redirigir a logout
                window.location.href = '/logout/';
            }
        }, 1000);
        
        // Renovar sesión al hacer click en botón
        const renewBtn = document.getElementById('renewSession');
        if (renewBtn) {
            renewBtn.addEventListener('click', () => {
                modal.hide();
                // Hacer request para mantener viva la sesión
                fetch('/', { method: 'HEAD' })
                    .then(() => {
                        resetInactivityTimer();
                    })
                    .catch(() => {
                        console.log('Error al renovar sesión');
                    });
            });
        }
    };
    
    // Detectar actividad del usuario
    const userActivityEvents = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
    
    userActivityEvents.forEach(event => {
        document.addEventListener(event, () => {
            resetInactivityTimer();
        }, true);
    });
    
    // Iniciar temporizador al cargar la página
    resetInactivityTimer();
});
