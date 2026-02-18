/* ================== SHORTCUT ================== */
const $ = id => document.getElementById(id);

/* ================== TEMPLATE MAP ================== */
const TEMPLATES = {
  academicYellow: {
    css: "../templates/template-academic-yellow/style.css",
    html: "../templates/template-academic-yellow/template.html"
  },
  professionalBlue: {
    css: "../templates/template-clean-profile/style.css",
    html: "../templates/template-clean-profile/template.html"
  },
  minimalElegant: {
    css: "../templates/template-modern-clean/style.css",
    html: "../templates/template-modern-clean/template.html"
  },
  blueCorporate: {
    css: "../templates/template-blue-corporate/style.css",
    html: "../templates/template-blue-corporate/template.html"
  },
  softGreenMinimal: {
    css: "../templates/template-soft-green-minimal/style.css",
    html: "../templates/template-soft-green-minimal/template.html"
  },
  darkElegant: {
    css: "../templates/template-dark-elegant/style.css",
    html: "../templates/template-dark-elegant/template.html"
  },
  timelineResume: {
    css: "../templates/template-timeline-resume/style.css",
    html: "../templates/template-timeline-resume/template.html"
  },
  boldRedAccent: {
    css: "../templates/template-Bold-red-Accent/style.css",
    html: "../templates/template-Bold-red-Accent/template.html"
  },
  cardBased: {
    css: "../templates/template-card-based/style.css",
    html: "../templates/template-card-based/template.html"
  },
  glassmorphism: {
    css: "../templates/template-glassmorphism/style.css",
    html: "../templates/template-glassmorphism/template.html"
  },
  infographic: {
    css: "../templates/template-infographic/style.css",
    html: "../templates/template-infographic/template.html"
  },
  ultraMinimal: {
    css: "../templates/template-ultra-minimal-black&white/style.css",
    html: "../templates/template-ultra-minimal-black&white/template.html"
  },
  boxShadow: {
    css: "../templates/template-box-shadow/style.css",
    html: "../templates/template-box-shadow/template.html"
  },
  classicSerif: {
    css: "../templates/template-classic-serif/style.css",
    html: "../templates/template-classic-serif/template.html"
  },
  freshGradient: {
    css: "../templates/template-fresh-gradient/style.css",
    html: "../templates/template-fresh-gradient/template.html"
  },
  splitHeaderModern: {
    css: "../templates/template-split-header-modern/style.css",
    html: "../templates/template-split-header-modern/template.html"
  },
  techLook: {
    css: "../templates/template-tech-look/style.css",
    html: "../templates/template-tech-look/template.html"
  },
  ultraClean: {
    css: "../templates/template-ultra-clean/style.css",
    html: "../templates/template-ultra-clean/template.html"
  }
};

/* ================== SELECTED TEMPLATE ================== */
const selectedTemplate =
  localStorage.getItem("selectedTemplate") || "academicYellow";

/* ================== LOAD TEMPLATE CSS ================== */
(function loadTemplateCSS() {
  if (document.getElementById("template-style")) return;

  const link = document.createElement("link");
  link.id = "template-style";
  link.rel = "stylesheet";
  link.href = TEMPLATES[selectedTemplate].css;
  document.head.appendChild(link);
})();

/* ================== LOAD TEMPLATE HTML ================== */
const templateRes = await fetch(TEMPLATES[selectedTemplate].html);
const html = await templateRes.text();
$("resumePreview").innerHTML = html;
loadHeader();
loadEducation();
loadExperience();
loadSkills();
loadCustomSections();
bindSkillButtons();
renderCustomSectionsList();

/* ================== HEADER (STEP-1) ================== */
function loadHeader() {
  const d = JSON.parse(localStorage.getItem("step1") || "{}");

  setText("previewName", d.name);
  setText("previewTitle", d.title);
  setText("previewSummary", d.summary);
  setText("previewPhone", d.phone);
  setText("previewEmail", d.email);
  setText("previewLocation", d.location);

  fillList("pLanguages", d.languages);
  fillList("pCerts", d.certs);
}

/* ================== EDUCATION (STEP-2) ================== */
function loadEducation() {
  const d = JSON.parse(localStorage.getItem("step2") || {});
  const section = $("educationSection");

  if (!section || !d.degree) {
    section?.classList.add("hide-section");
    return;
  }

  const dateText = d.current
    ? `Expected ${formatMonth(d.month)}`
    : formatMonth(d.month);

  const detailsList = d.details?.length
    ? "<ul>" + d.details.map(x => "<li>" + x + "</li>").join("") + "</ul>"
    : "";

  section.innerHTML = `
    <h3>EDUCATION</h3>
    <ul>
      <li>
        <strong>${d.degree} in ${d.field}</strong><br>
        ${d.school} | ${d.location}<br>
        <em>${dateText}</em>
        ${detailsList}
      </li>
    </ul>
  `;

  section.classList.remove("hide-section");
}

/* ================== EXPERIENCE (STEP-3) ================== */
function loadExperience() {
  const list = JSON.parse(localStorage.getItem("experiences") || "[]");
  const section = $("previewExperienceSection");
  const box = $("previewExperienceList");

  if (!section || !box) {
    console.warn("Experience section or list not found");
    return;
  }

  if (!list.length) {
    section.classList.add("hide-section");
    section.style.display = "none";
    return;
  }

  box.innerHTML = "";

  // Check if this is academic-yellow template (has experience-list class)
  const isAcademicYellow = box.classList.contains("experience-list");

  list.forEach(exp => {
    const citySep = exp.city && exp.country ? ", " : "";
    const dateSep = exp.startDate && exp.endDate ? " – " : "";
    const locationPart = exp.city || exp.country
      ? `<small>${exp.city || ""}${citySep}${exp.country || ""}</small><br>`
      : "";
    const datePart = exp.startDate || exp.endDate
      ? `<small>${exp.startDate || ""}${dateSep}${exp.endDate || ""}</small>`
      : "";
    const div = document.createElement("div");
    div.className = isAcademicYellow ? "mb-3" : "exp-item mb-3";
    div.innerHTML = `
      <strong>${exp.jobTitle}${exp.employer ? " – " + exp.employer : ""}</strong><br>
      ${locationPart}
      ${datePart}
      <ul>
        ${(exp.description || "")
          .split("\n")
          .filter(Boolean)
          .map(l => `<li>${l}</li>`)
          .join("")}
      </ul>
    `;
    box.appendChild(div);
  });

  // Show the section - ensure it's visible
  section.classList.remove("hide-section");
  section.style.display = "block";
  section.style.visibility = "visible";
  
  // Also ensure parent wrappers are visible (for academic-yellow)
  const contentBox = box.closest(".content-box");
  if (contentBox) {
    contentBox.style.display = "block";
    contentBox.style.visibility = "visible";
    contentBox.classList.remove("hide-section");
  }
  
  // Ensure section-title is visible (for academic-yellow)
  const sectionTitle = section.querySelector(".section-title");
  if (sectionTitle) {
    sectionTitle.style.display = "flex";
    sectionTitle.style.visibility = "visible";
  }
  
  console.log("Experience loaded:", list.length, "items", "Template:", isAcademicYellow ? "academic-yellow" : "other");
  console.log("Section display:", globalThis.getComputedStyle(section).display);
  console.log("Content box display:", contentBox ? globalThis.getComputedStyle(contentBox).display : "N/A");
}

/* ================== SKILLS (STEP-4) ================== */
function loadSkills() {
  const skills = JSON.parse(localStorage.getItem("skills") || "[]");
  const ul = $("previewSkills");

  if (!ul) return;

  const section = ul.closest("section");

  if (!skills.length) {
    section?.classList.add("hide-section");
    return;
  }

  ul.innerHTML = "";
  skills.forEach(skill => {
    const li = document.createElement("li");
    li.textContent = skill;
    ul.appendChild(li);
  });

  section?.classList.remove("hide-section");
}

$("skillsEditor")?.addEventListener("input", async e => {
  const lines = e.target.value.split("\n");
  const q = lines[lines.length - 1].trim();

  saveSkills(getSkills()); // ✅ save here (merged logic)
  loadSkills(); // ✅ Update live preview when typing

  if (q.length < 1) {
      const box = $("skillSuggestions");
      box.innerHTML = "";
      box.style.display = "none";
      return;
    }


  const res = await fetch(`/api/skills/suggest?q=${encodeURIComponent(q)}`);
  const suggestions = await res.json();

  const box = $("skillSuggestions");
  box.innerHTML = "";
  box.style.display = "block";

  suggestions.forEach(skill => {
    const div = document.createElement("div");
    div.className = "suggestion-item";
    div.textContent = skill;
    div.onclick = () => {
      lines[lines.length - 1] = skill;
      e.target.value = lines.join("\n") + "\n";
      box.innerHTML = "";
      saveSkills(getSkills());
      loadSkills(); // ✅ Update live preview when selecting suggestion
    };
    box.appendChild(div);
  });
});

/* ================== GET / SAVE / RESTORE SKILLS ================== */
function getSkills() {
  return $("skillsEditor").value
    .split("\n")
    .map(s => s.trim())
    .filter(Boolean);
}

function saveSkills(list) {
  localStorage.setItem("skills", JSON.stringify(list));
}

(function restoreSkills() {
  const list = JSON.parse(localStorage.getItem("skills") || "[]");
  if ($("skillsEditor")) {
    $("skillsEditor").value = list.join("\n");
  }
})();

/* ================== BIND SKILL BUTTONS ================== */
function bindSkillButtons() {
  document.querySelectorAll(".skill-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const skill = btn.dataset.skill;
      if (!skill) return;
      
      const editor = $("skillsEditor");
      if (!editor) return;
      
      // Get current skills
      const currentSkills = getSkills();
      
      // Check if skill already exists
      if (currentSkills.includes(skill)) {
        return; // Don't add duplicates
      }
      
      // Add skill to textarea
      const currentValue = editor.value.trim();
      const newValue = currentValue 
        ? currentValue + "\n" + skill
        : skill;
      
      editor.value = newValue;
      
      // Save and update preview
      saveSkills(getSkills());
      loadSkills();
    });
  });
}

/* ================== HELPERS ================== */
function setText(id, val) {
  const el = $(id);
  if (el) el.textContent = val || "";
}

function fillList(id, text) {
  const ul = $(id);
  if (!ul || !text) return;
  ul.innerHTML = text
    .split("\n")
    .filter(Boolean)
    .map(l => `<li>${l}</li>`)
    .join("");
}

function formatMonth(v) {
  if (!v) return "";
  return new Date(v).toLocaleDateString("en-US", {
    month: "short",
    year: "numeric"
  });
}

/* ================== CUSTOM SECTIONS ================== */
let editingCustomSectionIndex = null;

function getCustomSections() {
  return JSON.parse(localStorage.getItem("customSections") || "[]");
}

function saveCustomSections(sections) {
  localStorage.setItem("customSections", JSON.stringify(sections));
}

function showAddCustomSection() {
  editingCustomSectionIndex = null;
  $("customSectionName").value = "";
  $("customSectionDescription").value = "";
  $("customSectionModal").style.display = "flex";
  document.querySelector(".custom-section-modal .modal-content h5").textContent = "Add Custom Section";
}

function closeCustomSectionModal() {
  $("customSectionModal").style.display = "none";
  editingCustomSectionIndex = null;
}

function saveCustomSection() {
  const name = $("customSectionName").value.trim();
  const description = $("customSectionDescription").value.trim();

  if (!name || !description) {
    alert("Please fill in both section name and description.");
    return;
  }

  const sections = getCustomSections();

  if (editingCustomSectionIndex === null) {
    // Add new section
    sections.push({ name, description });
  } else {
    // Edit existing section
    sections[editingCustomSectionIndex] = { name, description };
  }

  saveCustomSections(sections);
  renderCustomSectionsList();
  loadCustomSections();
  closeCustomSectionModal();
}

function editCustomSection(index) {
  const sections = getCustomSections();
  if (sections[index]) {
    editingCustomSectionIndex = index;
    $("customSectionName").value = sections[index].name;
    $("customSectionDescription").value = sections[index].description;
    $("customSectionModal").style.display = "flex";
    document.querySelector(".custom-section-modal .modal-content h5").textContent = "Edit Custom Section";
  }
}

function deleteCustomSection(index) {
  if (confirm("Are you sure you want to delete this custom section?")) {
    const sections = getCustomSections();
    sections.splice(index, 1);
    saveCustomSections(sections);
    renderCustomSectionsList();
    loadCustomSections();
  }
}

function renderCustomSectionsList() {
  const sections = getCustomSections();
  const list = $("customSectionsList");
  
  if (!sections.length) {
    list.innerHTML = '<p class="text-light-gray small mb-0">No custom sections added yet.</p>';
    return;
  }

  list.innerHTML = sections.map((section, index) => `
    <div class="custom-section-item">
      <div class="custom-section-item-content">
        <div class="custom-section-item-title">${escapeHtml(section.name)}</div>
        <div class="custom-section-item-desc">${escapeHtml(section.description)}</div>
      </div>
      <div class="custom-section-item-actions">
        <button onclick="editCustomSection(${index})" title="Edit">
          <i class="bi bi-pencil"></i>
        </button>
        <button onclick="deleteCustomSection(${index})" title="Delete">
          <i class="bi bi-trash"></i>
        </button>
      </div>
    </div>
  `).join("");
}

function loadCustomSections() {
  const sections = getCustomSections();
  
  if (!sections.length) {
    // Remove existing custom sections if none exist
    document.querySelectorAll(".custom-section-preview").forEach(el => el.remove());
    return;
  }

  // Find the right panel (main content area)
  const rightPanel = document.querySelector(".right-panel") || document.querySelector("main") || document.querySelector(".content-column");
  
  if (!rightPanel) {
    console.warn("Could not find right panel for custom sections");
    return;
  }

  // Detect template type by checking existing section classes and structure
  const existingSection = rightPanel.querySelector(".main-section") || rightPanel.querySelector(".content-card") || rightPanel.querySelector(".card-content") || rightPanel.querySelector("section");
  let sectionClass = "main-section";
  let useWrapper = false;
  let wrapperClass = "";
  
  if (existingSection) {
    // Check for blue-corporate template (uses content-card)
    if (existingSection.classList.contains("content-card")) {
      sectionClass = "content-card";
    } 
    // Check for academic-yellow template (uses main-section card-content with inner structure)
    else if (existingSection.classList.contains("card-content")) {
      sectionClass = "main-section card-content";
      useWrapper = true;
      wrapperClass = "content-box";
    } 
    // Default to main-section
    else {
      sectionClass = "main-section";
    }
  }

  // Remove existing custom sections from preview
  document.querySelectorAll(".custom-section-preview").forEach(el => el.remove());

  // Add custom sections after experience section
  sections.forEach((section, index) => {
    const sectionEl = document.createElement("section");
    sectionEl.className = `${sectionClass} custom-section-preview`;
    sectionEl.id = `customSection${index}`;
    
    // Format description - handle newlines
    const listItems = section.description.split("\n").filter(Boolean).map(d => "<li>" + escapeHtml(d) + "</li>").join("");
    const descHtml = section.description.includes("\n")
      ? "<ul>" + listItems + "</ul>"
      : "<p style=\"white-space: pre-wrap;\">" + escapeHtml(section.description) + "</p>";
    
    // Check if template uses wrapper structure (like academic-yellow)
    if (useWrapper && wrapperClass) {
      sectionEl.innerHTML = `
        <div class="section-title">
          <span class="title-icon"></span>
          <h3>${escapeHtml(section.name.toUpperCase())}</h3>
        </div>
        <div class="${wrapperClass}">
          ${descHtml}
        </div>
      `;
    } else {
      sectionEl.innerHTML = `
        <h3>${escapeHtml(section.name.toUpperCase())}</h3>
        ${descHtml}
      `;
    }
    
    // Insert after experience section if it exists, otherwise append
    const experienceSection = rightPanel.querySelector("#previewExperienceSection");
    if (experienceSection) {
      // Insert after the experience section
      experienceSection.after(sectionEl);
    } else {
      // If no experience section, append to the end
      rightPanel.appendChild(sectionEl);
    }
  });
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

/* ================== FINAL SAVE ================== */
function finishResume() {
  const customSections = getCustomSections();
  console.log("Saving resume with custom sections:", customSections.length, customSections);
  
  // Generate descriptive title with template name and date
  const templateNames = {
    academicYellow: "Academic Yellow",
    professionalBlue: "Professional Blue",
    minimalElegant: "Minimal Elegant",
    blueCorporate: "Blue Corporate",
    softGreenMinimal: "Soft Green",
    darkElegant: "Dark Elegant",
    timelineResume: "Timeline",
    boldRedAccent: "Bold Red",
    cardBased: "Card Based",
    glassmorphism: "Glassmorphism",
    infographic: "Infographic",
    ultraMinimal: "Ultra Minimal",
    boxShadow: "Box Shadow",
    classicSerif: "Classic Serif",
    freshGradient: "Fresh Gradient",
    splitHeaderModern: "Split Header",
    techLook: "Tech Look",
    ultraClean: "Ultra Clean"
  };
  
  const templateDisplayName = templateNames[selectedTemplate] || selectedTemplate;
  const now = new Date();
  const dateStr = now.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  });
  const timeStr = now.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true 
  });
  
  // Auto-generate title: "Template Name - Date Time"
  const autoTitle = `${templateDisplayName} - ${dateStr} ${timeStr}`;
  
  const resumePayload = {
    title: autoTitle,
    template: selectedTemplate,
    data: {
      step1: JSON.parse(localStorage.getItem("step1") || "{}"),
      step2: JSON.parse(localStorage.getItem("step2") || "{}"),
      step3: JSON.parse(localStorage.getItem("experiences") || "[]"),
      step4: JSON.parse(localStorage.getItem("skills") || "[]"),
      customSections: customSections // ✅ Include custom sections
    }
  };
  
  console.log("Resume payload:", JSON.stringify(resumePayload, null, 2));

  fetch("/api/resumes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(resumePayload)
  })
    .then(res => res.json())
    .then(r => {
      if (r.success) globalThis.location.href = "/documents.html";
      else alert(r.message || "Save failed");
    });
}
