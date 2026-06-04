document.addEventListener("DOMContentLoaded", () => {
    // ==========================================
    // 1. SCROLL REVEAL ANIMATION (INTERACTIONS)
    // ==========================================
    const revealElements = document.querySelectorAll(".reveal");

    function revealOnScroll() {
        const triggerBottom = window.innerHeight * 0.88;

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
    revealOnScroll(); // Trigger once on load

    // ==========================================
    // 2. ACTIVE NAV HIGHLIGHTING
    // ==========================================
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-links a");

    navLinks.forEach((link) => {
        const href = link.getAttribute("href");
        if (href === currentPath || (href !== "/" && currentPath.startsWith(href))) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });

    // ==========================================
    // 3. CORE BUTTON INTERACTIVE MICRO-TRANSFORMS
    // ==========================================
    const buttons = document.querySelectorAll(".btn");
    buttons.forEach((btn) => {
        btn.addEventListener("mousedown", () => {
            btn.style.transform = "scale(0.96) translateY(-2px)";
        });
        btn.addEventListener("mouseup", () => {
            btn.style.transform = "";
        });
        btn.addEventListener("mouseleave", () => {
            btn.style.transform = "";
        });
    });

    // ==========================================
    // 4. FLOATING AI ASSISTANT CHATBOT INITIALIZER
    // ==========================================
    initializeChatbot();
});

// ==========================================
// 5. ROLE DROPDOWN SYSTEMS (IT / NON-IT)
// ==========================================
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

// ==========================================
// 6. FLOATING CHATBOT CORE LOGIC
// ==========================================
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
                <p>Hi 👋 I am your <strong>AI Resume Assistant</strong>!</p>
                <p>I can help you with:</p>
                <ul>
                    <li>Drafting summary statements</li>
                    <li>Analyzing job matching mechanics</li>
                    <li>Recommending targeted IT/Non-IT project ideas</li>
                </ul>
                <p>Type a question or select a quick shortcut chip below to get started!</p>
            </div>
        `;
        chat.innerHTML = welcomeMessage;
        saveChatMessages();
    }
}

function toggleChat() {
    const chatWindow = document.getElementById("chat-window");
    if (!chatWindow) return;

    const isOpen = chatWindow.classList.contains("open");
    if (isOpen) {
        chatWindow.classList.remove("open");
        // Wait for CSS slide transition, then close panel display
        setTimeout(() => {
            if (!chatWindow.classList.contains("open")) {
                chatWindow.style.display = "none";
            }
        }, 300);
        localStorage.setItem(CHAT_OPEN_KEY, "closed");
    } else {
        chatWindow.style.display = "flex";
        // Force reflow for CSS transitions
        chatWindow.offsetHeight;
        chatWindow.classList.add("open");
        localStorage.setItem(CHAT_OPEN_KEY, "open");
        scrollChatToBottom();
    }
}

function setMode(selectedMode) {
    mode = selectedMode;
    localStorage.setItem(CHAT_MODE_KEY, mode);
    highlightSelectedModeButton();
}

function highlightSelectedModeButton() {
    const buttons = document.querySelectorAll(".chat-actions button");
    buttons.forEach((btn) => {
        btn.classList.remove("active");
    });

    let targetId = "btn-mode-chat";
    if (mode === "resume") targetId = "btn-mode-resume";
    else if (mode === "rewrite") targetId = "btn-mode-rewrite";

    const selectedBtn = document.getElementById(targetId);
    if (selectedBtn) {
        selectedBtn.classList.add("active");
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

    // Render premium dynamic typing indicator dots
    const loading = document.createElement("div");
    loading.className = "ai-msg";
    loading.innerHTML = `
        <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
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
        
        // Render with markdown parsing format support
        appendAiMessage(data.reply || "No response received from assistant.");
    } catch (error) {
        loading.remove();
        appendAiMessage("⚠️ <strong>Server Connection Error:</strong> Unable to reach the assistant. Please ensure the backend server is running.");
    }
}

function sendSuggestedPrompt(promptText) {
    const input = document.getElementById("chat-input");
    if (!input) return;
    input.value = promptText;
    sendMessage();
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

    chat.innerHTML += `<div class="ai-msg">${formatMarkdown(message)}</div>`;
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
        chatWindow.classList.add("open");
    } else {
        chatWindow.style.display = "none";
        chatWindow.classList.remove("open");
    }
}

// Simple Parser for basic markdown in AI responses
function formatMarkdown(text) {
    if (!text) return "";
    let formatted = text;
    
    // Bold: **text** -> <strong>text</strong>
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
    
    // Italic: *text* -> <em>text</em>
    formatted = formatted.replace(/\*(.*?)\*/g, "<em>$1</em>");
    
    // New lines to HTML br
    formatted = formatted.replace(/\n/g, "<br>");
    
    // Lists: Bullet lines starting with '- ' or '• ' -> wrapped in standard HTML list tags (handled cleanly via br or custom inline styling)
    formatted = formatted.replace(/(?:^|<br>)[-•]\s+(.*?)(?=$|<br>)/g, "$1");
    
    return formatted;
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// Enter Key listeners
document.addEventListener("keydown", function (e) {
    const input = document.getElementById("chat-input");
    if (e.key === "Enter" && document.activeElement === input) {
        e.preventDefault();
        sendMessage();
    }
});