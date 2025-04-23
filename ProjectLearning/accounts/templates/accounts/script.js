document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", function () {
            // Убираем активный класс у всех вкладок и содержимого
            tabs.forEach(t => t.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));

            // Добавляем активный класс к текущей вкладке и её содержимому
            this.classList.add("active");
            tabContents[index].classList.add("active");
        });
    });

    // Устанавливаем активной первую вкладку при загрузке
    if (tabs.length > 0) {
        tabs[0].classList.add("active");
        tabContents[0].classList.add("active");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const chatInput = document.getElementById("chat-input");
    const chatSend = document.getElementById("chat-send");

    chatSend.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        const messageText = chatInput.value.trim();
        if (messageText === "") return;

        const userName = "Вы"; // Можно заменить на реального пользователя
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", "user-message");

        messageDiv.innerHTML = `<span class="author">${userName}</span>${messageText}`;
        chatMessages.appendChild(messageDiv);

        chatInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight; // Прокрутка вниз
    }
});
