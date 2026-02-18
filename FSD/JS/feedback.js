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

document.getElementById("feedbackForm").addEventListener("submit", async e => {
  e.preventDefault();

  const name = document.getElementById("fbName").value.trim();
  const email = document.getElementById("fbEmail").value.trim();
  const rating = document.getElementById("rating").value;
  const message = document.getElementById("fbMessage").value.trim();

  if (!name || !email || !rating || !message) {
    alert("Please fill all fields");
    return;
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
      alert(data.msg || "Failed to submit feedback");
      return;
    }

    alert("Thank you for your feedback!");
    e.target.reset();

  } catch (err) {
    console.error(err);
    alert("Server unavailable");
  }
});