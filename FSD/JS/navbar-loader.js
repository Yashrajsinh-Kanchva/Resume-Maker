// FSD/JS/navbar-loader.js
fetch("/navbar.html")
  .then(res => res.text())
  .then(html => {
    const container = document.getElementById("navbar-container");
    if (!container) return;
    container.innerHTML = html;
    setActiveNav();
    loadNavbarUser(); // 👈 important
    attachLogoutHandler(container);
    initNavbarDropdowns(container);
  });

function attachLogoutHandler(container) {
  container.addEventListener("click", function (e) {
    const logoutLink = e.target.closest('a[href="/logout"]');
    if (!logoutLink) return;
    e.preventDefault();
    fetch("/logout", { credentials: "include" })
      .then(function () {
        window.location.href = "/login";
      })
      .catch(function () {
        window.location.href = "/login";
      });
  });
}

/** Initialize Bootstrap dropdowns in injected navbar (they are added after Bootstrap may have run). */
function initNavbarDropdowns(container) {
  function init() {
    if (typeof bootstrap === "undefined") return;
    container.querySelectorAll("[data-bs-toggle=\"dropdown\"]").forEach(function (el) {
      new bootstrap.Dropdown(el);
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}

function setActiveNav() {
  const currentPage = window.location.pathname.split("/").pop();

  document.querySelectorAll(".nav-link").forEach(link => {
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active");
    }
  });
}

async function loadNavbarUser() {
  try {
    const res = await fetch("/api/users/me", { credentials: "include" });
    if (!res.ok) return;

    const data = await res.json();

    const usernameEl = document.getElementById("username");

    if (usernameEl && data.user) {
      const name = data.user.name || "User";
      const id = data.user.id || "";
      // Update username - show name only (remove id if not needed)
      usernameEl.textContent = name;
    }

  } catch (err) {
    console.error("Navbar user fetch failed", err);
  }
}

// Make function globally accessible for other scripts
window.loadNavbarUser = loadNavbarUser;
