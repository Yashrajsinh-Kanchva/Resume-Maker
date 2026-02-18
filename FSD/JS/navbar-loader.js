// FSD/JS/navbar-loader.js
const navRes = await fetch("/navbar.html");
const html = await navRes.text();
const container = document.getElementById("navbar-container");
if (container) {
  container.innerHTML = html;
  setActiveNav();
  try {
    const userRes = await fetch("/api/users/me", { credentials: "include" });
    if (userRes.ok) {
      const data = await userRes.json();
      const usernameEl = document.getElementById("username");
      if (usernameEl && data.user) {
        usernameEl.textContent = data.user.name || "User";
      }
    }
  } catch (err) {
    console.error("Navbar user fetch failed", err);
  }
  attachLogoutHandler(container);
  initNavbarDropdowns(container);
}

function attachLogoutHandler(container) {
  container.addEventListener("click", function (e) {
    const logoutLink = e.target.closest('a[href="/logout"]');
    if (!logoutLink) return;
    e.preventDefault();
    fetch("/logout", { credentials: "include" })
      .then(function () {
        globalThis.location.href = "/login";
      })
      .catch(function () {
        globalThis.location.href = "/login";
      });
  });
}

/** Initialize Bootstrap dropdowns in injected navbar (they are added after Bootstrap may have run). */
function initNavbarDropdowns(container) {
  function init() {
    if (typeof bootstrap === "undefined") return;
    container.querySelectorAll("[data-bs-toggle=\"dropdown\"]").forEach(function (el) {
      el.bootstrapDropdown = new bootstrap.Dropdown(el);
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}

function setActiveNav() {
  const currentPage = globalThis.location.pathname.split("/").pop();

  document.querySelectorAll(".nav-link").forEach(link => {
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active");
    }
  });
}

/** Re-fetch and display navbar user (e.g. after login). Exposed for other scripts. */
async function loadNavbarUser() {
  try {
    const res = await fetch("/api/users/me", { credentials: "include" });
    if (!res.ok) return;
    const data = await res.json();
    const usernameEl = document.getElementById("username");
    if (usernameEl && data.user) {
      usernameEl.textContent = data.user.name || "User";
    }
  } catch (err) {
    console.error("Navbar user fetch failed", err);
  }
}

globalThis.loadNavbarUser = loadNavbarUser;
