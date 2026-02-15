// 1. Configuración de APIs (Microservicios)
const ms_projects = "http://127.0.0.1:8000/projects";
const ms_leaders = "http://127.0.0.1:8001/leaders";

// Variables globales para almacenar líderes
let lideresDisponibles = [];

// --- 1. FUNCIÓN PARA MOSTRAR SECCIONES ---
function mostrarSeccion(seccion) {
    const secciones = document.querySelectorAll('.seccion');
    secciones.forEach(s => s.style.display = 'none');
    
    const inicio = document.getElementById('inicio');
    const proyectosDiv = document.getElementById('seccion-proyectos');
    const registrarDiv = document.getElementById('seccion-registrar');
    const contactoDiv = document.getElementById('seccion-contacto');
    const lideresDiv = document.getElementById('seccion-lideres');

    if (seccion === 'inicio' && inicio) {
        inicio.style.display = 'block';
    } 
    else if (seccion === 'proyectos' && proyectosDiv) {
        proyectosDiv.style.display = 'block'; 
        cargar(); 
    } 
    else if (seccion === 'registrar' && registrarDiv) {
        registrarDiv.style.display = 'block';
        cargarLideres(); // Cargar líderes para el formulario
    } 
    else if (seccion === 'contacto' && contactoDiv) {
        contactoDiv.style.display = 'block';
    }
    else if (seccion === 'lideres' && lideresDiv) {
        lideresDiv.style.display = 'block';
        cargarLideresUI(); // Cargar y mostrar líderes
    }
}

// --- 1.5 CARGAR LÍDERES DESDE MS-LEADERS ---
async function cargarLideres() {
    const selectLider = document.getElementById("lider");
    if (!selectLider) return;
    
    try {
        console.log("Cargando líderes desde:", ms_leaders);
        const res = await fetch(ms_leaders + "/");
        
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        
        lideresDisponibles = await res.json();
        console.log("Líderes obtenidos:", lideresDisponibles);
        
        selectLider.innerHTML = '<option value="">-- Selecciona un líder --</option>';
        
        if (lideresDisponibles && lideresDisponibles.length > 0) {
            lideresDisponibles.forEach(l => {
                const option = document.createElement('option');
                option.value = l.id;
                option.textContent = l.nombre;
                selectLider.appendChild(option);
            });
        } else {
            selectLider.innerHTML = '<option value="">No hay líderes disponibles</option>';
            console.warn("No se encontraron líderes");
        }
    } catch (error) {
        console.error("Error al cargar líderes:", error);
        selectLider.innerHTML = '<option value="">Error cargando líderes</option>';
        alert("Error al cargar líderes: " + error.message + "\n\nVerifica que MS-Leaders esté corriendo en puerto 8001");
    }
}

// --- 2. FUNCIÓN PARA CARGAR PROYECTOS ---
async function cargar() {
    const lista = document.getElementById("lista");
    if (!lista) return;

    lista.innerHTML = '<tr><td colspan="6" class="text-center py-4">Cargando datos...</td></tr>';

    try {
        const res = await fetch(ms_projects + "/"); 
        const data = await res.json();
        let filas = "";
        
        if (!data || data.length === 0) {
            filas = `<tr><td colspan="6" class="text-center py-5 text-muted">No hay proyectos aún.</td></tr>`;
        } else {
            data.forEach(p => {
                const fechaFormat = p.fecha_inicio 
                    ? new Date(p.fecha_inicio).toLocaleDateString('es-ES') 
                    : 'Sin fecha';

                const estadoBadge = p.estado 
                    ? '<span class="badge bg-success">Activo</span>'
                    : '<span class="badge bg-secondary">Finalizado</span>';
                
                // Obtener nombre del líder desde los datos enriquecidos
                const nombreLider = p.lider ? p.lider.nombre : 'Sin líder';
                
                filas += `<tr>
                            <td><strong>#${p.id}</strong></td>
                            <td><strong>${p.titulo}</strong></td>
                            <td><i class="fas fa-user-tie me-1"></i> ${nombreLider}</td>
                            <td>${fechaFormat}</td>
                            <td>${estadoBadge}</td>
                            <td class="text-center">
                                <button class="btn btn-sm btn-outline-danger" onclick="eliminarProyecto(${p.id})">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </td>
                          </tr>`;
            });
        }
        lista.innerHTML = filas;
    } catch (error) {
        console.error("Error al cargar:", error);
        lista.innerHTML = `<tr><td colspan="6" class="text-center py-5 text-danger">Error de conexión con ms-projects.</td></tr>`;
    }
}

// --- 3. FUNCIÓN PARA ELIMINAR PROYECTO ---
async function eliminarProyecto(id) {
    if (!confirm("¿Estás seguro de que deseas eliminar este proyecto?")) return;

    try {
        const res = await fetch(`${ms_projects}/${id}`, {
            method: "DELETE"
        });

        if (res.ok) {
            alert("Proyecto eliminado correctamente");
            cargar(); 
        } else {
            console.error("Error del servidor:", res.status);
            alert(`Error ${res.status}: El servidor no permitió borrar el proyecto.`);
        }
    } catch (error) {
        console.error("Error de conexión:", error);
        alert("Error de conexión: Asegúrate de que ms-projects esté corriendo en puerto 8000.");
    }
}

// --- 4. EVENTO PARA REGISTRAR PROYECTO ---
const form = document.getElementById("formProyecto");
if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const btn = e.target.querySelector('button');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
        btn.disabled = true;
        
        try {
            const liderSelect = document.getElementById("lider");
            const lider_id = parseInt(liderSelect.value);
            
            if (!lider_id) {
                alert('Por favor selecciona un líder');
                btn.innerHTML = originalText;
                btn.disabled = false;
                return;
            }
            
            const nuevo = {
                titulo: document.getElementById("titulo").value,
                lider_id: lider_id,
                fecha_inicio: document.getElementById("fecha").value, // Formato ISO YYYY-MM-DD
                descripcion: document.getElementById("desc").value,
                estado: true 
            };

            console.log("Enviando proyecto:", nuevo);

            const res = await fetch(ms_projects + "/", { 
                method: "POST", 
                headers: { "Content-Type": "application/json" }, 
                body: JSON.stringify(nuevo) 
            });
            
            if (res.ok) {
                alert('¡Proyecto guardado exitosamente!');
                e.target.reset();
                mostrarSeccion('proyectos'); 
            } else {
                let errorMsg = 'Error desconocido';
                try {
                    const errorData = await res.json();
                    errorMsg = errorData.detail || JSON.stringify(errorData);
                } catch (e) {
                    errorMsg = `Error HTTP ${res.status}`;
                }
                console.error('Error guardando proyecto:', errorMsg);
                alert(`Error: ${errorMsg}`);
            }
        } catch (error) {
            console.error('Error al guardar:', error);
            alert('Error al guardar: ' + error.message);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });
}

// --- 4.5 CARGAR Y MOSTRAR LISTA DE LÍDERES EN UI ---
async function cargarLideresUI() {
    const listaLideres = document.getElementById("listaLideres");
    if (!listaLideres) return;
    
    try {
        console.log("Cargando lista de líderes desde:", ms_leaders);
        listaLideres.innerHTML = '<p class="text-muted">Cargando líderes...</p>';
        
        const res = await fetch(ms_leaders + "/");
        
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        
        const lideres = await res.json();
        console.log("Líderes obtenidos para UI:", lideres);
        
        if (!lideres || lideres.length === 0) {
            listaLideres.innerHTML = '<p class="text-muted">No hay líderes registrados aún.</p>';
            return;
        }
        
        // Crear tabla HTML para mostrar líderes
        let html = `
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Departamento</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        lideres.forEach(l => {
            html += `
                <tr>
                    <td><small class="text-muted">${l.id}</small></td>
                    <td><strong>${l.nombre}</strong></td>
                    <td>${l.email}</td>
                    <td>${l.departamento}</td>
                    <td>
                        <button class="btn btn-sm btn-danger" onclick="eliminarLider(${l.id})">
                            Eliminar
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        listaLideres.innerHTML = html;
    } catch (error) {
        console.error("Error al cargar lista de líderes:", error);
        listaLideres.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
}

// --- 4.6 ELIMINAR LÍDER ---
async function eliminarLider(id) {
    if (!confirm('¿Estás seguro de que quieres eliminar este líder?')) return;
    
    try {
        const res = await fetch(ms_leaders + "/" + id, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            alert('Líder eliminado exitosamente');
            cargarLideresUI(); // Actualizar lista
            cargarLideres();   // Actualizar dropdown de proyectos
        } else {
            const error = await res.json();
            alert(`Error: ${error.detail}`);
        }
    } catch (error) {
        console.error(error);
        alert('Error al eliminar: ' + error.message);
    }
}

// --- 4.7 CREAR NUEVO LÍDER ---
document.addEventListener('DOMContentLoaded', () => {
    const formLider = document.getElementById("formLider");
    
    if (formLider) {
        formLider.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const nombreLider = document.getElementById("nombreLider").value.trim();
            const emailLider = document.getElementById("emailLider").value.trim();
            const deptLider = document.getElementById("deptLider").value.trim();
            
            if (!nombreLider || !emailLider || !deptLider) {
                alert('Por favor completa todos los campos');
                return;
            }
            
            const btn = e.target.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;
            btn.innerHTML = 'Creando...';
            btn.disabled = true;
            
            try {
                console.log("Enviando nuevo líder:", { nombreLider, emailLider, deptLider });
                
                const res = await fetch(ms_leaders + "/", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        nombre: nombreLider,
                        email: emailLider,
                        departamento: deptLider
                    })
                });
                
                if (res.ok) {
                    const nuevoLider = await res.json();
                    console.log("Líder creado:", nuevoLider);
                    alert('¡Líder creado exitosamente!');
                    formLider.reset();
                    cargarLideresUI(); // Actualizar lista de líderes
                    cargarLideres();   // Actualizar dropdown de proyectos
                } else {
                    const error = await res.json();
                    alert(`Error: ${error.detail || 'No se pudo crear el líder'}`);
                }
            } catch (error) {
                console.error(error);
                alert('Error al crear líder: ' + error.message);
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        });
    }
});

// --- 5. MOSTRAR SECCIÓN DE LÍDERES ---
function mostrarSeccionLideres() {
    const seccion = document.getElementById('seccion-lideres');
    if (seccion) {
        const secciones = document.querySelectorAll('.seccion');
        secciones.forEach(s => s.style.display = 'none');
        seccion.style.display = 'block';
        cargarLideresUI(); // Cargar y mostrar líderes
    }
}

// --- 6. INICIO AUTOMÁTICO ---
window.addEventListener('load', async () => {
    mostrarSeccion('inicio');
    // Cargar líderes al iniciar para tenerlos listos
    // await cargarLideres(); // Comentado: solo se carga cuando se accede a 'Registrar'
});