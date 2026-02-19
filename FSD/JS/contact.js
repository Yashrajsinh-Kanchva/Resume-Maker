/* ===============================
   FAQ TOGGLE
================================ */
document.querySelectorAll(".faq-question").forEach(btn => {
  btn.addEventListener("click", () => {
    btn.parentElement.classList.toggle("active");
  });
});

/* ===============================
   AUTO LOAD USER DATA
================================ */
try {
  const userRes = await fetch("/api/users/me", { credentials: "include" });
  if (userRes.ok) {
    const data = await userRes.json();
    if (data.authenticated && data.user) {
      document.getElementById("fullName").value = data.user.name || "";
      document.getElementById("email").value = data.user.email || "";
    }
  }
} catch (err) {
  console.error("User fetch failed", err);
}

/* ===============================
   CONTACT FORM SUBMIT
================================ */
const contactForm = document.getElementById("contactForm");
if (contactForm) {
    contactForm.addEventListener("submit", async e => {
      e.preventDefault();

      const name = document.getElementById("fullName").value.trim();
      const email = document.getElementById("email").value.trim();
      const subject = document.getElementById("subject").value;
      const message = document.getElementById("message").value.trim();

      if (!name || !email || !subject || !message) {
        alert("Please fill all fields");
        return;
      }

      try {
        const res = await fetch("/api/contact/send", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({
            name,
            email,
            subject,
            message
          })
        });

        const data = await res.json();

        if (!res.ok) {
          alert(data.msg || "Failed to send message");
          return;
        }

        alert("Message sent successfully!");
        document.getElementById("message").value = "";
        document.getElementById("subject").value = "";

      } catch (err) {
        console.error("Contact error:", err);
        alert("Mail service unavailable.");
      }
    });
}

/* ===============================
   ROBOT EYES FOLLOW CURSOR
================================ */
const robot = document.getElementById("robotAssistant");
const pupils = document.querySelectorAll(".pupil");

document.addEventListener("mousemove", e => {
  if (!robot) return;

  const rect = robot.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;

  const angle = Math.atan2(e.clientY - centerY, e.clientX - centerX);
  const x = Math.cos(angle) * 5;
  const y = Math.sin(angle) * 5;

  pupils.forEach(pupil => {
    pupil.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
  });
});

/* ===============================
   CHATBOT LOGIC (MAPPED TO NEW UI)
================================ */
const chatWidget = document.getElementById("chatWidget");
const closeChat = document.getElementById("closeChat");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const chatBody = document.getElementById("chatBody");

// Toggle Widget Visibility
if (robot) {
  robot.addEventListener("click", () => {
    // Replaced 'prompt' with Widget toggle
    chatWidget.classList.toggle("active");
    if (chatWidget.classList.contains("active")) {
        setTimeout(() => chatInput.focus(), 300);
    }
  });
}

if (closeChat) {
    closeChat.addEventListener("click", () => {
        chatWidget.classList.remove("active");
    });
}

// Helper to add messages to UI
function addMessage(text, className) {
    const div = document.createElement("div");
    div.classList.add(className);
    div.innerText = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Send Message Logic (Using YOUR fetch logic)
async function sendMessage() {
    const userText = chatInput.value.trim();
    if (!userText) return;

    // 1. Show user message
    addMessage(userText, "user-msg");
    chatInput.value = "";

    try {
        // 2. Call your existing API
        const res = await fetch("/api/chat/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userText })
        });

        const data = await res.json();

        // 3. Show bot response
        if (data.reply) {
            addMessage(data.reply, "bot-msg");
        } else {
            addMessage("No response from server.", "bot-msg");
        }

        // 4. Handle intents
        if (data.intent === "SCROLL_FAQ") {
            document.getElementById("faq")?.scrollIntoView({ behavior: "smooth" });
        } else if (data.intent === "GO_TO_FEEDBACK") {
            // Navigate to feedback page after a short delay
            setTimeout(() => {
                globalThis.location.href = "feedback.html";
            }, 1000);
        }

    } catch (err) {
        console.error("Chatbot error:", err);
        addMessage("Chat service unavailable.", "bot-msg");
    }
}

// Event Listeners for Send
if (sendBtn) sendBtn.addEventListener("click", sendMessage);

if (chatInput) {
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
}