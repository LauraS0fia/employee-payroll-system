// Obtener todos los items del menú
const menuItems = document.querySelectorAll('.menu-item');
const sections = document.querySelectorAll('.section');

// Función para cambiar de sección
function changeSection(sectionId) {
    // Ocultar todas las secciones
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Remover clase active de todos los items del menú
    menuItems.forEach(item => {
        item.classList.remove('active');
    });

    // Mostrar la sección seleccionada
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Agregar clase active al item del menú seleccionado
    const activeMenuItem = document.querySelector(`[data-section="${sectionId}"]`);
    if (activeMenuItem) {
        activeMenuItem.classList.add('active');
    }
}

// Agregar event listener a cada item del menú
menuItems.forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault();
        const sectionId = this.getAttribute('data-section');
        changeSection(sectionId);
    });
});