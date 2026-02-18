// =======================================
// FADE-IN ANIMATION (UNCHANGED)
// =======================================
const sections = document.querySelectorAll(".fade-section");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
      }
    });
  },
  { threshold: 0.15 }
);

sections.forEach(section => observer.observe(section));


// =======================================
// AUTH CHECK – FETCH LOGGED-IN USER
// =======================================
try {
  const response = await fetch("/api/users/me", {
    method: "GET",
    credentials: "include"
  });

  if (!response.ok) throw new Error("User not authenticated");

  const data = await response.json();

  const usernameEl = document.getElementById("username");
  const firstNameEl = document.getElementById("firstName");

  if (usernameEl) usernameEl.textContent = data.user.name;
  if (firstNameEl) firstNameEl.textContent = data.user.name.split(" ")[0];

} catch (error) {
  console.error("Auth check failed:", error);
  globalThis.location.href = "loginPage.html";
}


// =======================================
// LOGOUT
// =======================================
function logoutUser() {
  fetch("/logout", { credentials: "include" })
    .finally(() => globalThis.location.href = "loginPage.html");
}


// =======================================
// FETCH & DISPLAY USER REVIEWS (FIXED)
// =======================================
document.addEventListener("DOMContentLoaded", () => {
  fetchReviews();
});

async function fetchReviews() {
  try {
    const res = await fetch("/api/feedbacks", {
      credentials: "include"
    });

    if (!res.ok) return;

    const reviews = await res.json();
    const container = document.getElementById("reviewsContainer");

    if (!container) return;

    container.innerHTML = "";

    reviews.forEach(review => {
      const col = document.createElement("div");
        col.className = "col-md-4 mb-4";


      col.innerHTML = `
  <div class="quote-card">
    <div class="quote-icon">"</div>

    <p class="quote-text">
      ${escapeHtml(review.feedback)}
    </p>

    <div class="quote-divider"></div>

    <div class="quote-name">
      ${escapeHtml(review.name)}
    </div>
  </div>
`;


      container.appendChild(col);
    });

  } catch (err) {
    console.error("Failed to load reviews:", err);
  }
}


// =======================================
// XSS SAFETY
// =======================================
function escapeHtml(text) {
  return text.replaceAll(/[&<>"']/g, ch => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[ch]));
}

document.getElementById("checkScoreBtn").addEventListener("click", async () => {

  const response = await fetch("/api/resume-score", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(globalThis.resumePayload)
  });

  const data = await response.json();
  document.getElementById("resumeScore").innerText = data.resume_score;
});
