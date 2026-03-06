/**
 * Sistema de paginación reutilizable para tablas
 * Uso: new TablePagination('tableId', 'paginationId', rowsPerPage)
 */
class TablePagination {
    constructor(tableId, paginationContainerId, rowsPerPage = 10) {
        this.table = document.getElementById(tableId);
        if (!this.table) {
            console.error(`Tabla con id "${tableId}" no encontrada`);
            return;
        }
        
        this.tbody = this.table.querySelector('tbody');
        this.rows = Array.from(this.tbody.rows);
        this.paginationContainer = document.getElementById(paginationContainerId);
        this.rowsPerPage = rowsPerPage;
        this.currentPage = 1;
        this.filteredRows = this.rows;
    }

    displayPage(filteredRows = null) {
        if (filteredRows !== null) {
            this.filteredRows = filteredRows;
        }

        // Ocultar todas las filas
        this.rows.forEach(row => row.style.display = "none");

        const start = (this.currentPage - 1) * this.rowsPerPage;
        const end = start + this.rowsPerPage;

        // Mostrar filas de la página actual
        this.filteredRows.slice(start, end).forEach(row => {
            row.style.display = "";
        });
    }

    setupPagination(filteredRows = null) {
        if (filteredRows !== null) {
            this.filteredRows = filteredRows;
        }

        const totalPages = Math.ceil(this.filteredRows.length / this.rowsPerPage) || 1;

        this.paginationContainer.innerHTML = `
            <button class="btn btn-primary btn-sm" id="prevBtn" ${this.currentPage === 1 ? 'disabled' : ''}>Anterior</button>
            <span class="p-2">Página ${this.currentPage} de ${totalPages}</span>
            <button class="btn btn-primary btn-sm" id="nextBtn" ${this.currentPage === totalPages ? 'disabled' : ''}>Siguiente</button>
        `;

        const prevBtn = document.getElementById("prevBtn");
        const nextBtn = document.getElementById("nextBtn");

        if (prevBtn) {
            prevBtn.onclick = () => {
                if (this.currentPage > 1) {
                    this.currentPage--;
                    this.displayPage();
                    this.setupPagination();
                }
            };
        }

        if (nextBtn) {
            nextBtn.onclick = () => {
                if (this.currentPage < totalPages) {
                    this.currentPage++;
                    this.displayPage();
                    this.setupPagination();
                }
            };
        }
    }

    reset() {
        this.currentPage = 1;
        this.filteredRows = this.rows;
    }

    filter(filterFunction) {
        this.filteredRows = this.rows.filter(filterFunction);
        this.currentPage = 1;
        this.displayPage();
        this.setupPagination();
    }

    init() {
        this.displayPage();
        this.setupPagination();
    }
}
