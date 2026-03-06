/**
 * Sistema de filtros para tablas con búsqueda y filtros por columna
 */
class TableFilters {
    constructor(config) {
        this.searchInputId = config.searchInputId;
        this.tableId = config.tableId;
        this.selectFilterId = config.selectFilterId || null;
        this.selectFilterColumn = config.selectFilterColumn || null;
        this.clearBtnId = config.clearBtnId || null;
        this.pagination = config.pagination || null;

        this.searchInput = document.getElementById(this.searchInputId);
        this.table = document.getElementById(this.tableId);
        this.selectFilter = this.selectFilterId ? document.getElementById(this.selectFilterId) : null;
        this.clearBtn = this.clearBtnId ? document.getElementById(this.clearBtnId) : null;

        if (!this.table) {
            console.error(`Tabla con id "${this.tableId}" no encontrada`);
            return;
        }

        this.rows = Array.from(this.table.querySelector('tbody').rows);
        this.init();
    }

    init() {
        // Configurar evento de búsqueda
        if (this.searchInput) {
            this.searchInput.addEventListener("keyup", () => this.applyFilters());
        }

        // Configurar filtro de select
        if (this.selectFilter) {
            this.selectFilter.addEventListener("change", () => this.applyFilters());
            this.populateSelectFilter();
        }

        // Configurar botón de limpiar
        if (this.clearBtn) {
            this.clearBtn.addEventListener("click", () => this.clearFilters());
        }
    }

    populateSelectFilter() {
        if (!this.selectFilter || this.selectFilterColumn === null) return;

        const uniqueValues = new Set();
        this.rows.forEach(row => {
            const cell = row.cells[this.selectFilterColumn];
            if (cell) {
                const value = cell.innerText.trim();
                if (value) uniqueValues.add(value);
            }
        });

        [...uniqueValues].sort().forEach(value => {
            const option = document.createElement("option");
            option.value = value.toLowerCase();
            option.textContent = value;
            this.selectFilter.appendChild(option);
        });
    }

    applyFilters() {
        const searchText = this.searchInput ? this.searchInput.value.toLowerCase() : "";
        const selectValue = this.selectFilter ? this.selectFilter.value : "";

        const filtered = this.rows.filter(row => {
            const rowText = row.innerText.toLowerCase();
            const matchesSearch = rowText.includes(searchText);

            let matchesSelect = true;
            if (this.selectFilter && selectValue && this.selectFilterColumn !== null) {
                const cellValue = row.cells[this.selectFilterColumn].innerText.toLowerCase();
                matchesSelect = cellValue === selectValue;
            }

            return matchesSearch && matchesSelect;
        });

        if (this.pagination) {
            this.pagination.currentPage = 1;
            this.pagination.displayPage(filtered);
            this.pagination.setupPagination(filtered);
        } else {
            // Si no hay paginación, mostrar/ocultar directamente
            this.rows.forEach(row => row.style.display = "none");
            filtered.forEach(row => row.style.display = "");
        }
    }

    clearFilters() {
        if (this.searchInput) this.searchInput.value = "";
        if (this.selectFilter) this.selectFilter.value = "";

        if (this.pagination) {
            this.pagination.reset();
            this.pagination.displayPage();
            this.pagination.setupPagination();
        } else {
            this.rows.forEach(row => row.style.display = "");
        }
    }
}
