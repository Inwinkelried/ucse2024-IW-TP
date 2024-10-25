document.addEventListener("DOMContentLoaded", function() {
    const messageModal = new bootstrap.Modal(document.getElementById('messageModal'));
    
    // Comprobar si hay mensajes y abrir el modal
    const messages = document.getElementById('messages').value; // Usar un input oculto para pasar los mensajes
    if (messages) {
        messageModal.show();
    }
});


document.addEventListener("DOMContentLoaded", function() {
    // Obtener los mensajes del input oculto
    const messages = document.getElementById("messages").value;
    
    // Si hay mensajes, muestra el modal
    if (messages) {
        // Crear el contenido del modal
        const messageList = messages.split(', ').map(msg => `<li class="alert alert-info">${msg}</li>`).join('');
        document.getElementById("modal-message-content").innerHTML = `<ul class="list-unstyled">${messageList}</ul>`;
        
        // Mostrar el modal
        const messageModal = new bootstrap.Modal(document.getElementById("messageModal"));
        messageModal.show();
    }
});

