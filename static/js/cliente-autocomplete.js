/**
 * Autocompletado de datos del cliente por RUT o nombre
 * Requiere: URL de búsqueda configurada en el template
 */
document.addEventListener("DOMContentLoaded", function () {
    const clienteInput = document.getElementById("id_cliente");
    const rutInput = document.getElementById("id_rut_cliente");
    
    if (!rutInput || !clienteInput) return;

    const estadoRut = document.createElement("small");
    estadoRut.className = "text-muted d-block mt-1";
    rutInput.parentElement.appendChild(estadoRut);

    const campos = {
        cliente: document.getElementById("id_cliente"),
        giro: document.getElementById("id_giro"),
        telefono: document.getElementById("id_telefono"),
        direccion: document.getElementById("id_direccion"),
        comuna: document.getElementById("id_comuna"),
        ciudad: document.getElementById("id_ciudad"),
        lugar_de_entrega: document.getElementById("id_lugar_de_entrega"),
        persona_responsable: document.getElementById("id_persona_responsable")
    };

    const buscarCliente = async () => {
        const rut = rutInput.value.trim();
        const nombre = clienteInput.value.trim();

        if (!rut && !nombre) {
            estadoRut.textContent = "";
            return;
        }

        try {
            estadoRut.textContent = "Buscando cliente...";
            const params = new URLSearchParams();
            if (rut) params.set("rut", rut);
            if (nombre) params.set("nombre", nombre);
            params.set("_ts", Date.now().toString());

            // URL debe ser configurada en el template
            const buscarClienteUrl = window.BUSCAR_CLIENTE_URL || '/pedidos/buscar-cliente/';
            const response = await fetch(`${buscarClienteUrl}?${params.toString()}`, {
                cache: "no-store"
            });
            
            if (!response.ok) {
                estadoRut.textContent = "No se pudo consultar el cliente.";
                return;
            }

            const data = await response.json();
            if (!data.found) {
                estadoRut.textContent = "Cliente no encontrado para ese RUT o nombre.";
                return;
            }

            Object.keys(campos).forEach((key) => {
                if (campos[key] && data.cliente[key] !== undefined) {
                    campos[key].value = data.cliente[key] || "";
                }
            });

            estadoRut.textContent = "Cliente encontrado. Datos autocompletados.";
        } catch (error) {
            estadoRut.textContent = "Error al consultar el cliente.";
        }
    };

    rutInput.addEventListener("blur", buscarCliente);
    clienteInput.addEventListener("blur", buscarCliente);

    // Cálculo automático de totales
    const netoInput = document.getElementById("id_neto") || document.getElementById("neto");
    const ivaInput = document.getElementById("id_iva") || document.getElementById("iva");
    const totalInput =
        document.getElementById("id_total") ||
        document.getElementById("id_total_general") ||
        document.getElementById("total_general") ||
        document.getElementById("total");

    const parseMonto = (valor) => {
        if (!valor) return 0;
        const normalizado = valor.toString().replace(/\./g, "").replace(",", ".").replace(/[^\d.-]/g, "");
        const numero = Number(normalizado);
        return Number.isFinite(numero) ? numero : 0;
    };

    const actualizarTotalGeneral = () => {
        if (!netoInput || !ivaInput || !totalInput) return;
        const neto = parseMonto(netoInput.value);
        const iva = parseMonto(ivaInput.value);
        const total = neto + iva;
        totalInput.value = total.toFixed(2);
    };

    if (netoInput && ivaInput && totalInput) {
        netoInput.addEventListener("input", actualizarTotalGeneral);
        ivaInput.addEventListener("input", actualizarTotalGeneral);
        actualizarTotalGeneral();
    }
});
