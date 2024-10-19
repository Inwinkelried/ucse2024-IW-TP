document.addEventListener("DOMContentLoaded", function() {
    const messageModal = new bootstrap.Modal(document.getElementById('messageModal'));
    
    // Comprobar si hay mensajes y abrir el modal
    const messages = document.getElementById('messages').value; // Usar un input oculto para pasar los mensajes
    if (messages) {
        messageModal.show();
    }
});
