/* ================== SHORTCUT ================== */
const $ = id => document.getElementById(id);

/* ================== TEMPLATE MAP ================== */
const TEMPLATES = {
  academicYellow: {
    css: "../templates/template-academic-yellow/style.css",
    html: "../templates/template-academic-yellow/template.html"
  },
  professionalBlue: { // template 2
    css: "../templates/template-clean-profile/style.css",
    html: "../templates/template-clean-profile/template.html"
  },
  minimalElegant: { // template 3
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
loadExperience();
restoreEducation();

/* ================== LOAD HEADER (STEP-1) ================== */
function loadHeader() {
  const d = JSON.parse(localStorage.getItem("step1") || "{}");

  setText("previewName", d.name);
  setText("previewTitle", d.title);
  setText("previewEmail", d.email);
  setText("previewPhone", d.phone);
  setText("previewLocation", d.location);
  setText("previewSummary", d.summary);

  fillList("pLanguages", d.languages);
  fillList("pCerts", d.certs);
}

/* ================== EXPERIENCE (STEP-2 DATA) ================== */
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

/* ================== EDUCATION (STEP-3) ================== */

/* LIVE SAVE */
[
  "school",
  "eduLocation",
  "degree",
  "field",
  "gradMonth",
  "currentStudy",
  "eduDetails"
].forEach(id => {
  const el = $(id);
  if (!el) return;
  el.addEventListener("input", saveEducation);
  el.addEventListener("change", saveEducation);
});

/* SAVE EDUCATION */
function saveEducation() {
  const data = {
    school: $("school")?.value.trim() || "",
    location: $("eduLocation")?.value.trim() || "",
    degree: $("degree")?.value.trim() || "",
    field: $("field")?.value.trim() || "",
    month: $("gradMonth")?.value || "",
    current: $("currentStudy")?.checked || false,
    details: ($("eduDetails")?.value || "")
      .split("\n")
      .map(x => x.trim())
      .filter(Boolean)
  };

  localStorage.setItem("step2", JSON.stringify(data));
  renderEducation(data);
}

/* RESTORE EDUCATION */
function restoreEducation() {
  const raw = localStorage.getItem("step2");
  if (!raw) return;

  let d;
  try {
    d = JSON.parse(raw);
  } catch {
    console.error("Invalid step2 data");
    return;
  }

  if ($("school")) $("school").value = d.school || "";
  if ($("eduLocation")) $("eduLocation").value = d.location || "";
  if ($("degree")) $("degree").value = d.degree || "";
  if ($("field")) $("field").value = d.field || "";
  if ($("gradMonth")) $("gradMonth").value = d.month || "";
  if ($("currentStudy")) $("currentStudy").checked = d.current || false;
  if ($("eduDetails")) $("eduDetails").value = (d.details || []).join("\n");

  renderEducation(d);
}

/* RENDER EDUCATION TO PREVIEW */
function renderEducation(d) {
  const section = $("educationSection");
  if (!section || !d.school) return;

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

/* ================== NAV ================== */
function goToStep4() {
  saveEducation();
  globalThis.location.href = "step-4.html";
}
globalThis.goToStep4 = goToStep4;
function saveExperiences(list) {
  localStorage.setItem("experiences", JSON.stringify(list));
  loadExperience(); // 🔥 refresh preview
}
