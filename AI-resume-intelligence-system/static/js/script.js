document.addEventListener("DOMContentLoaded", () => {
    // =========================
    // SCROLL REVEAL ANIMATION
    // =========================
    const revealElements = document.querySelectorAll(".reveal");

    function revealOnScroll() {
        const triggerBottom = window.innerHeight * 0.85;

        revealElements.forEach((element) => {
            const boxTop = element.getBoundingClientRect().top;

            if (boxTop < triggerBottom) {
                element.classList.add("active");
            } else {
                element.classList.remove("active");
            }
        });
    }

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll();

    // =========================
    // ACTIVE NAV LINK
    // =========================
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-links a");

    navLinks.forEach((link) => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });

    // =========================
    // BUTTON CLICK EFFECT
    // =========================
    const buttons = document.querySelectorAll(".btn");

    buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
            btn.style.transform = "scale(0.95)";
            setTimeout(() => {
                btn.style.transform = "";
            }, 150);
        });
    });

    // =========================
    // CHATBOT INIT
    // =========================
    initializeChatbot();
});


// =========================
// ROLE DROPDOWN SYSTEM
// =========================
function getCareerRoles(category) {
    const roles = {
        "IT": [
            "Software Developer",
            "Web Developer",
            "Data Analyst",
            "AI / ML Engineer",
            "Cybersecurity Analyst"
        ],
        "Non-IT": [
            "Core Engineer",
            "Design Engineer",
            "Site / Project Engineer",
            "Operations Executive",
            "Business Analyst"
        ]
    };

    return roles[category] || [];
}

function updateRoles() {
    const categoryElement = document.getElementById("category");
    const roleDropdown = document.getElementById("role");

    if (!categoryElement || !roleDropdown) return;

    const category = categoryElement.value;
    roleDropdown.innerHTML = '<option value="">Select Career Path</option>';

    getCareerRoles(category).forEach((role) => {
        const option = document.createElement("option");
        option.value = role;
        option.text = role;
        roleDropdown.appendChild(option);
    });
}

function updateRolesForJobMatch() {
    const categoryElement = document.getElementById("category");
    const roleDropdown = document.getElementById("job_role");

    if (!categoryElement || !roleDropdown) return;

    const category = categoryElement.value;
    roleDropdown.innerHTML = '<option value="">Select Career Path</option>';

    getCareerRoles(category).forEach((role) => {
        const option = document.createElement("option");
        option.value = role;
        option.text = role;
        roleDropdown.appendChild(option);
    });
}


// =========================
// FLOATING CHATBOT SYSTEM
// =========================
let mode = "chat";

const CHAT_STORAGE_KEY = "ai_resume_chat_history";
const CHAT_MODE_KEY = "ai_resume_chat_mode";
const CHAT_OPEN_KEY = "ai_resume_chat_open";

function initializeChatbot() {
    const chat = document.getElementById("chat-messages");
    if (!chat) return;

    restoreChatMode();
    restoreChatMessages();
    restoreChatWindowState();
    highlightSelectedModeButton();

    if (chat.innerHTML.trim() === "") {
        const welcomeMessage = `
            <div class="ai-msg">
                Hi 👋 I can help with resume writing, rewriting, jobs, skills, and career guidance.
            </div>
        `;
        chat.innerHTML = welcomeMessage;
        saveChatMessages();
    }
}

function toggleChat() {
    const chatWindow = document.getElementById("chat-window");
    if (!chatWindow) return;

    const isOpen = chatWindow.style.display === "flex";
    chatWindow.style.display = isOpen ? "none" : "flex";

    localStorage.setItem(CHAT_OPEN_KEY, isOpen ? "closed" : "open");
}

function setMode(selectedMode) {
    mode = selectedMode;
    localStorage.setItem(CHAT_MODE_KEY, mode);
    highlightSelectedModeButton();
}

function highlightSelectedModeButton() {
    const buttons = document.querySelectorAll(".chat-actions button");

    buttons.forEach((btn) => {
        btn.style.background = "#1e293b";
        btn.style.color = "#e2e8f0";
    });

    const selected = Array.from(buttons).find(
        (btn) => btn.innerText.trim().toLowerCase() === mode
    );

    if (selected) {
        selected.style.background = "#60a5fa";
        selected.style.color = "#06111f";
    }
}

async function sendMessage() {
    const input = document.getElementById("chat-input");
    const chat = document.getElementById("chat-messages");

    if (!input || !chat) return;

    const msg = input.value.trim();
    if (!msg) return;

    appendUserMessage(msg);
    input.value = "";

    const loading = document.createElement("div");
    loading.className = "ai-msg";
    loading.innerText = "Typing...";
    chat.appendChild(loading);
    scrollChatToBottom();

    try {
        const res = await fetch("/ai-assistant", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: msg,
                mode: mode
            })
        });

        const data = await res.json();

        loading.remove();
        appendAiMessage(data.reply || "No response received.");
    } catch (error) {
        loading.remove();
        appendAiMessage("⚠️ Server error");
    }
}

function appendUserMessage(message) {
    const chat = document.getElementById("chat-messages");
    if (!chat) return;

    chat.innerHTML += `<div class="user-msg">${escapeHtml(message)}</div>`;
    saveChatMessages();
    scrollChatToBottom();
}

function appendAiMessage(message) {
    const chat = document.getElementById("chat-messages");
    if (!chat) return;

    chat.innerHTML += `<div class="ai-msg">${escapeHtml(message)}</div>`;
    saveChatMessages();
    scrollChatToBottom();
}

function scrollChatToBottom() {
    const chat = document.getElementById("chat-messages");
    if (!chat) return;

    chat.scrollTop = chat.scrollHeight;
}

function saveChatMessages() {
    const chat = document.getElementById("chat-messages");
    if (!chat) return;

    localStorage.setItem(CHAT_STORAGE_KEY, chat.innerHTML);
}

function restoreChatMessages() {
    const chat = document.getElementById("chat-messages");
    if (!chat) return;

    const savedMessages = localStorage.getItem(CHAT_STORAGE_KEY);
    if (savedMessages) {
        chat.innerHTML = savedMessages;
        scrollChatToBottom();
    }
}

function restoreChatMode() {
    const savedMode = localStorage.getItem(CHAT_MODE_KEY);
    if (savedMode) {
        mode = savedMode;
    }
}

function restoreChatWindowState() {
    const chatWindow = document.getElementById("chat-window");
    if (!chatWindow) return;

    const savedState = localStorage.getItem(CHAT_OPEN_KEY);
    if (savedState === "open") {
        chatWindow.style.display = "flex";
    } else {
        chatWindow.style.display = "none";
    }
}

function clearChatSession() {
    localStorage.removeItem(CHAT_STORAGE_KEY);
    localStorage.removeItem(CHAT_MODE_KEY);
    localStorage.removeItem(CHAT_OPEN_KEY);

    const chat = document.getElementById("chat-messages");
    if (chat) {
        chat.innerHTML = `
            <div class="ai-msg">
                Hi 👋 I can help with resume writing, rewriting, jobs, skills, and career guidance.
            </div>
        `;
    }

    mode = "chat";
    highlightSelectedModeButton();
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}


// =========================
// ENTER KEY SUPPORT
// =========================
document.addEventListener("keydown", function (e) {
    const input = document.getElementById("chat-input");

    if (e.key === "Enter" && document.activeElement === input) {
        e.preventDefault();
        sendMessage();
    }
});