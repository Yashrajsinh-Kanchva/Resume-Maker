/* ===============================
   AUTO LOAD USER DATA FROM DATABASE
================================ */
try {
  const res = await fetch("/api/users/me", {
    credentials: "include"
  });

  if (res.ok) {
    const data = await res.json();

    if (data.authenticated && data.user) {
      const nameField = document.getElementById("fbName");
      const emailField = document.getElementById("fbEmail");

      if (nameField && data.user.name) {
        nameField.value = data.user.name || "";
      }
      if (emailField && data.user.email) {
        emailField.value = data.user.email || "";
      }
    }
  }
} catch (err) {
  console.error("User fetch failed", err);
}

function showFeedbackStatus(message, isSuccess) {
  const el = document.getElementById("feedbackFormStatus");
  if (!el) return;
  el.textContent = message;
  el.className = "feedback-form-status mt-3 " + (isSuccess ? "feedback-form-status--success" : "feedback-form-status--error");
  el.style.display = "block";
  el.setAttribute("role", "alert");
  setTimeout(() => {
    el.style.display = "none";
    el.removeAttribute("role");
  }, 5000);
}

document.getElementById("feedbackForm").addEventListener("submit", async e => {
  e.preventDefault();

  const name = document.getElementById("fbName").value.trim();
  const email = document.getElementById("fbEmail").value.trim();
  const rating = document.getElementById("rating").value;
  const message = document.getElementById("fbMessage").value.trim();
  const statusEl = document.getElementById("feedbackFormStatus");
  if (statusEl) statusEl.style.display = "none";

  if (!name || !email || !rating || !message) {
    showFeedbackStatus("Please fill in all fields.", false);
    return;
  }

  const form = e.target;
  const submitBtn = form.querySelector('button[type="submit"]');
  const originalText = submitBtn ? submitBtn.innerHTML : "";
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Submitting...';
  }

  try {
    const res = await fetch("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ name, email, rating, message })
    });

    const data = await res.json();

    if (!res.ok) {
      showFeedbackStatus(data.msg || "Failed to submit feedback. Please try again.", false);
      return;
    }

    showFeedbackStatus("Thank you! Your feedback has been reported successfully.", true);
    form.reset();

  } catch (err) {
    console.error(err);
    showFeedbackStatus("Unable to submit. Please check your connection and try again.", false);
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  }
});