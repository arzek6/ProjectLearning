document.addEventListener("DOMContentLoaded", function () {
    function getCSRFToken() {
        const cookie = document.cookie.match(/csrftoken=([\w-]+)/);
        return cookie ? cookie[1] : '';
    }
    // === Tabs ===
    const tabs = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", function () {
            tabs.forEach(t => t.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));
            this.classList.add("active");
            tabContents[index].classList.add("active");
        });
    });

    if (tabs.length > 0) {
        tabs[0].classList.add("active");
        tabContents[0].classList.add("active");
    }

// === Chat ===

const chatInput = document.getElementById('chat-input');
const chatSendBtn = document.getElementById('chat-send');
const chatTumbler= document.getElementById('chat');
const chatMessages = document.getElementById('chat-messages');
const fileInput = document.getElementById('chat-file');
const fileNameText = document.getElementById('file-name-text');
const projectId = window.location.pathname.split('/')[2];

// === Обработка выбора файла ===
if (fileInput && fileNameText) {
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            fileNameText.textContent = fileInput.files[0].name;
        } else {
            fileNameText.textContent = "Прикрепить файл";
        }
    });
}
if (chatTumbler) {
    chatTumbler.addEventListener('click', function () {
function fetchMessages() {
    fetch(`/project/${projectId}/chat/messages/`)
        .then(response => response.json())
        .then(data => {
            chatMessages.innerHTML = '';

            let lastDate = null;

            data.forEach(msg => {
                const messageDate = msg.timestamp.split(' ')[0];
                if (messageDate !== lastDate) {
                    const dateDivider = document.createElement('div');
                    dateDivider.className = 'chat-date-divider';
                    dateDivider.textContent = messageDate;
                    chatMessages.appendChild(dateDivider);
                    lastDate = messageDate;
                }

                const isYou = msg.sender === currentUsername;

                const messageBubble = document.createElement('div');
                messageBubble.className = `chat-message ${isYou ? 'you' : 'other'}`;

                const sender = document.createElement('div');
                sender.className = 'sender';
                sender.textContent = msg.sender;

                const messageText = document.createElement('div');
                messageText.className = 'message-text';
                messageText.textContent = msg.message;

                const timestamp = document.createElement('div');
                timestamp.className = 'timestamp';
                timestamp.textContent = msg.timestamp;

                messageBubble.appendChild(sender);
                messageBubble.appendChild(messageText);

                if (msg.file_url) {
                    const fileLink = document.createElement('a');
                    fileLink.href = msg.file_url;
                    fileLink.target = "_blank";
                    fileLink.className = "chat-file-link";

                    const icon = document.createElement('span');
                    icon.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" 
                             fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path d="M21.44 11.05 12.05 20.44a5.5 5.5 0 1 1-7.78-7.78l9.19-9.19
                            a3.5 3.5 0 0 1 4.95 4.95l-9.2 9.19a1.5 1.5 0 0 1-2.12-2.12l8.49-8.49"/>
                        </svg>
                    `;

                    const name = document.createElement('span');
                    name.textContent = msg.file_name ? msg.file_name : "Неизвестный файл";

                    fileLink.appendChild(icon);
                    fileLink.appendChild(name);
                    messageBubble.appendChild(fileLink);
                }

                messageBubble.appendChild(timestamp);
                chatMessages.appendChild(messageBubble);
            });

            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
}

if (chatSendBtn) {
    chatSendBtn.addEventListener('click', function () {
        const message = chatInput.value.trim();
        const file = fileInput.files[0];

        if (!message && !file) return;

        const formData = new FormData();
        formData.append('message', message);
        if (file) formData.append('file', file);

        fetch(`/project/${projectId}/chat/send/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка сервера при отправке сообщения");
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'ok') {
                chatInput.value = '';
                fileInput.value = '';
                fileNameText.textContent = "Прикрепить файл";
                fetchMessages();
            }
        })
        .catch(error => {
            console.error("Ошибка при отправке:", error);
        });

    });
}

function getCSRFToken() {
    const cookie = document.cookie.match(/csrftoken=([\w-]+)/);
    return cookie ? cookie[1] : '';
}

setInterval(fetchMessages, 5000);
fetchMessages();
});
}

    // === User Dropdown ===
    const userButton = document.getElementById("userButton");
    const dropdownMenu = document.getElementById("dropdownMenu");

    if (userButton && dropdownMenu) {
        userButton.addEventListener("click", function (event) {
            event.stopPropagation();
            dropdownMenu.classList.toggle("show");
        });

        document.addEventListener("click", function (event) {
            if (!dropdownMenu.contains(event.target) && event.target !== userButton) {
                dropdownMenu.classList.remove("show");
            }
        });
    }

    // === Project Search ===
    const searchInput = document.getElementById("projectSearch");
    const projectsList = document.getElementById("projectsList");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value;

            fetch(`/projects/?q=${encodeURIComponent(query)}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(response => response.text())
                .then(data => {
                    const parser = new DOMParser();
                    const htmlDoc = parser.parseFromString(data, "text/html");
                    const newList = htmlDoc.getElementById("projectsList");

                    if (newList) {
                        projectsList.innerHTML = newList.innerHTML;
                    }
                })
                .catch(error => {
                    console.error("Ошибка при поиске:", error);
                });
        });
    }

    // === Tasks check box ===
    document.querySelectorAll('.task-checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            const isChecked = this.checked;

            fetch('/task/toggle/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken()
                },
                body: `task_id=${taskId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'ok') {
                    alert('Ошибка при обновлении задачи');
                    this.checked = !isChecked;
                }
            })
            .catch(err => {
                console.error('Ошибка:', err);
                this.checked = !isChecked;
            });
        });
    });

    // === Remove participants ===
    document.querySelectorAll('.remove-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            const userId = this.dataset.userId;

            if (confirm("Вы уверены, что хотите удалить этого участника?")) {
                fetch(`/project/${projectId}/remove_member/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: `user_id=${userId}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'ok') {
                        this.closest('li').remove();
                    } else {
                        alert('Ошибка при удалении участника');
                    }
                });
            }
        });
    });

    // === Invite participant ===
    const inviteForm = document.getElementById("invite-form");
    const inviteEmail = document.getElementById("invite-email");
    const inviteStatus = document.getElementById("invite-status");

    if (inviteForm) {
        inviteForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const email = inviteEmail.value.trim();

            fetch(`/project/${projectId}/invite_member/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken()
                },
                body: `email=${email}`
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    inviteStatus.textContent = "Участник приглашён!";
                    inviteEmail.value = '';
                } else {
                    inviteStatus.textContent = "Ошибка: " + data.message;
                }
            });
        });
    }

});
