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

  // Load latest 3 feedbacks (call here so it runs; DOMContentLoaded may have already fired with type="module")
  fetchReviews();
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
// FETCH & DISPLAY LATEST 3 FEEDBACKS (3 divs: name + feedback)
// =======================================

function renderStars(rating) {
  const n = Math.min(5, Math.max(0, Number(rating) || 0));
  const full = "★".repeat(n);
  const empty = "☆".repeat(5 - n);
  return `<span class="quote-rating" aria-label="Rating: ${n} out of 5">${full}${empty}</span>`;
}

async function fetchReviews() {
  const container = document.getElementById("reviewsContainer");
  if (!container) return;

  try {
    const res = await fetch("/api/feedbacks", { credentials: "include" });

    if (!res.ok) {
      showReviewsEmpty(container);
      return;
    }

    const reviews = await res.json();
    container.innerHTML = "";

    if (!Array.isArray(reviews) || reviews.length === 0) {
      showReviewsEmpty(container);
      return;
    }

    // Show first 3 latest feedbacks in 3 sections
    const toShow = reviews.slice(0, 3);
    toShow.forEach((review) => {
      const col = document.createElement("div");
      col.className = "col-md-4 mb-4";
      col.innerHTML = `
  <div class="quote-card">
    <div class="quote-icon">"</div>
    ${renderStars(review.rating)}
    <p class="quote-text">${escapeHtml(review.feedback || "")}</p>
    <div class="quote-divider"></div>
    <div class="quote-name">${escapeHtml(review.name || "User")}</div>
  </div>
`;
      container.appendChild(col);
    });
  } catch (err) {
    console.error("Failed to load reviews:", err);
    showReviewsEmpty(container);
  }
}

function showReviewsEmpty(container) {
  container.innerHTML = `
    <div class="col-12 text-center py-4">
      <p class="text-muted mb-0">No feedback yet. Be the first to share your experience!</p>
    </div>
  `;
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
