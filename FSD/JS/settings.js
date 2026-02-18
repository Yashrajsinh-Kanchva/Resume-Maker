/* ================= SETTINGS PAGE JAVASCRIPT ================= */

// Load user profile data when page loads
document.addEventListener("DOMContentLoaded", async function() {
  await loadUserProfile();
});

// Load user profile from API
async function loadUserProfile() {
  try {
    const response = await fetch("/api/users/profile", {
      credentials: "include"
    });

    if (!response.ok) {
      if (response.status === 401) {
        globalThis.location.href = "/loginPage.html";
        return;
      }
      throw new Error("Failed to load profile");
    }

    const data = await response.json();
    
    if (data.success && data.user) {
      // Populate form fields
      document.getElementById("userName").value = data.user.name || "";
      document.getElementById("userEmail").value = data.user.email || "";
      
      // Update provider badge
      const providerBadge = document.getElementById("providerBadge");
      const providerText = document.getElementById("providerText");
      
      if (data.user.provider === "google") {
        providerBadge.innerHTML = '<i class="bi bi-google me-2"></i><span>Google Account</span>';
        providerText.textContent = "Google Account";
      } else {
        providerBadge.innerHTML = '<i class="bi bi-person me-2"></i><span>Local Account</span>';
        providerText.textContent = "Local Account";
      }
    }
  } catch (error) {
    console.error("Error loading profile:", error);
    showMessage("Error loading profile. Please try again.", "danger");
  }
}

// Handle form submission
document.getElementById("profileForm")?.addEventListener("submit", async function(e) {
  e.preventDefault();
  
  const saveBtn = document.getElementById("saveBtn");
  const userName = document.getElementById("userName").value.trim();
  
  // Validate name
  if (!userName) {
    showMessage("Please enter your name", "danger");
    return;
  }
  
  if (userName.length < 2) {
    showMessage("Name must be at least 2 characters long", "danger");
    return;
  }
  
  // Show loading state
  const originalBtnText = saveBtn.innerHTML;
  saveBtn.disabled = true;
  saveBtn.classList.add("btn-loading");
  saveBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Saving...';
  
  try {
    const response = await fetch("/api/users/profile", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      credentials: "include",
      body: JSON.stringify({
        name: userName
      })
    });
    
    const data = await response.json();
    
    if (response.ok && data.success) {
      showMessage("Profile updated successfully!", "success");
      
      // Update the name field to show the saved value immediately
      document.getElementById("userName").value = userName;
      
      // Force reload navbar to reflect new name (with multiple retries)
      await refreshNavbar();
      
      // Retry navbar update after a short delay to ensure session is fully saved
      setTimeout(async () => {
        await refreshNavbar();
      }, 500);
    } else {
      throw new Error(data.message || "Failed to update profile");
    }
  } catch (error) {
    console.error("Error updating profile:", error);
    showMessage(error.message || "Error updating profile. Please try again.", "danger");
  } finally {
    // Reset button state
    saveBtn.disabled = false;
    saveBtn.classList.remove("btn-loading");
    saveBtn.innerHTML = originalBtnText;
  }
});

function getNavbarUserLoader() {
  if (typeof loadNavbarUser === "function") return loadNavbarUser;
  if (typeof globalThis.loadNavbarUser === "function") return globalThis.loadNavbarUser;
  return null;
}

function setNavbarUsername(name) {
  const usernameEl = document.getElementById("username");
  if (!usernameEl || !name) return;
  usernameEl.textContent = name;
  console.log("✅ Navbar username updated to:", name);
}

function setNavbarUsernameFromForm() {
  const usernameEl = document.getElementById("username");
  const userNameInput = document.getElementById("userName");
  if (!usernameEl || !userNameInput) return false;
  const name = userNameInput.value.trim();
  if (!name) return false;
  usernameEl.textContent = name;
  console.log("✅ Navbar username updated from form value:", name);
  return true;
}

async function refreshNavbar() {
  try {
    await new Promise(resolve => setTimeout(resolve, 300));

    const loader = getNavbarUserLoader();
    if (loader) {
      await loader();
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    const userResponse = await fetch("/api/users/me", { credentials: "include" });
    if (userResponse.ok) {
      const userData = await userResponse.json();
      const name = userData?.user?.name;
      if (name) setNavbarUsername(name);
    }

    setNavbarUsernameFromForm();
  } catch (error) {
    console.error("Error refreshing navbar:", error);
    setNavbarUsernameFromForm();
  }
}

// Show alert message
function showMessage(message, type) {
  const alertDiv = document.getElementById("messageAlert");
  const messageText = document.getElementById("messageText");
  
  // Remove existing alert classes
  alertDiv.classList.remove("alert-success", "alert-danger");
  
  // Add appropriate class
  alertDiv.classList.add(`alert-${type}`);
  
  // Set message
  messageText.textContent = message;
  
  // Show alert
  alertDiv.style.display = "block";
  alertDiv.classList.add("show");
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    alertDiv.classList.remove("show");
    setTimeout(() => {
      alertDiv.style.display = "none";
    }, 300);
  }, 5000);
  
  // Scroll to top to show message
  window.scrollTo({ top: 0, behavior: "smooth" });
}
