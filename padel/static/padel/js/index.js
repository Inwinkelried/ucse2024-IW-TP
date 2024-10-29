document.addEventListener("DOMContentLoaded", function() {
    const messageModal = new bootstrap.Modal(document.getElementById('messageModal'));
    
    
    const messages = document.getElementById('messages').value; 
    if (messages) {
        messageModal.show();
    }
});


document.addEventListener("DOMContentLoaded", function() {
    
    const messages = document.getElementById("messages").value;
    
 
    if (messages) {
       
        const messageList = messages.split(', ').map(msg => `<li class="alert alert-info">${msg}</li>`).join('');
        document.getElementById("modal-message-content").innerHTML = `<ul class="list-unstyled">${messageList}</ul>`;
        
    
        const messageModal = new bootstrap.Modal(document.getElementById("messageModal"));
        messageModal.show();
    }
});

