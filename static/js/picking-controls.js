/**
 * Controles para picking y descarga de PDF
 */

// Función para descargar PDF
function descargarPDF(notaId) {
    // Construir URL (debe ser configurada en el template)
    const baseUrl = window.DESCARGAR_PICKING_PDF_URL || '/pedidos/descargar-picking-pdf/';
    const url = baseUrl.replace('0', notaId);
    const btnDownload = event.target;
    const btnText = btnDownload.textContent;
    
    // Feedback visual: cambiar texto del botón
    btnDownload.disabled = true;
    btnDownload.textContent = 'Descargando...';
    
    // Crear un enlace temporal para descargar
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/pdf',
        }
    })
        .then(response => {
            if (response.status >= 300 && response.status < 400) {
                throw new Error(`Error de redirección: ${response.status}. Posiblemente sesión expirada.`);
            }
            
            if (!response.ok) {
                throw new Error(`Error en descarga: ${response.status} ${response.statusText}`);
            }
            
            return response.blob();
        })
        .then(blob => {
            if (blob.type !== 'application/pdf') {
                throw new Error('La respuesta no es un PDF válido');
            }
            
            const urlBlob = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = urlBlob;
            a.download = `picking_nota_${notaId}.pdf`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(urlBlob);
            
            btnDownload.disabled = false;
            btnDownload.textContent = btnText;
        })
        .catch(error => {
            console.error('Error descargando PDF:', error);
            alert(`Error al descargar el PDF: ${error.message}`);
            btnDownload.disabled = false;
            btnDownload.textContent = btnText;
        });
}

// Control del botón de término de picking
document.addEventListener('DOMContentLoaded', function() {
    const btnTerminoPicking = document.getElementById('btn-termino-picking');
    const formTerminoPicking = document.getElementById('termino-picking-form');
    
    if (btnTerminoPicking && formTerminoPicking) {
        if (btnTerminoPicking.disabled) {
            return;
        }
        
        formTerminoPicking.addEventListener('submit', function(e) {
            btnTerminoPicking.disabled = true;
            btnTerminoPicking.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Procesando...';
            
            setTimeout(function() {
                if (!document.body.classList.contains('form-submitted')) {
                    btnTerminoPicking.disabled = false;
                    btnTerminoPicking.innerHTML = 'Término de Picking';
                }
            }, 30000);
            
            document.body.classList.add('form-submitted');
        });
    }
});
