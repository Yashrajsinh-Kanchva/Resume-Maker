/* ================== SHORTCUT ================== */
const $ = id => document.getElementById(id);

/* ================== TEMPLATE CONFIG ================== */
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
renderExperiences();

/* ================== LOAD HEADER FROM STEP-1 ================== */
function loadHeader() {
  const d = JSON.parse(localStorage.getItem("step1") || "{}");

  setText("previewName", d.name);
  setText("previewTitle", d.title);
  setText("previewEmail", d.email);
  setText("previewPhone", d.phone);
  setText("previewLocation", d.location);
  setText("previewSummary", d.summary);

  fillList("pLanguages", d.languages || "English\nHindi");
  fillList("pCerts", d.certs || "Google Data Analytics\nAdvanced Excel");
}

/* ================== EXPERIENCE STORAGE ================== */
function getExperiences() {
  return JSON.parse(localStorage.getItem("experiences") || "[]");
}

function saveExperiences(arr) {
  localStorage.setItem("experiences", JSON.stringify(arr));
}

/* ================== DATE FORMAT ================== */
function formatMonth(val) {
  if (!val) return "";
  const d = new Date(val);
  return d.toLocaleDateString("en-US", {
    month: "short",
    year: "numeric"
  });
}

/* ================== ADD EXPERIENCE ================== */
$("addExperienceBtn")?.addEventListener("click", () => {
  const jobTitle = $("jobTitle")?.value.trim();
  const employer = $("employer")?.value.trim();
  const city = $("city")?.value.trim();
  const country = $("country")?.value.trim();
  const start = $("startDate")?.value;
  const end = $("endDate")?.value;
  const desc = $("description")?.value.trim();

  if (!jobTitle || !employer || !start || !end || !desc) {
    alert("Please fill all experience fields.");
    return;
  }

  const exp = {
    jobTitle,
    employer,
    city,
    country,
    startDate: formatMonth(start),
    endDate: formatMonth(end),
    description: desc
  };

  const list = getExperiences();
  list.unshift(exp); // most recent first
  saveExperiences(list);

  renderExperiences();
  clearForm();
});

/* ================== RENDER EXPERIENCE PREVIEW ================== */
function renderExperiences() {
  const list = getExperiences();
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

  // Clear existing content
  box.innerHTML = "";

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
    div.className = "mb-3";
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
  
  const templateKind = box.classList.contains("experience-list") ? "academic-yellow" : "other";
  console.log("Experience rendered:", list.length, "items", "Template:", templateKind);
  console.log("Section display:", globalThis.getComputedStyle(section).display);
  console.log("Content box display:", contentBox ? globalThis.getComputedStyle(contentBox).display : "N/A");
}

/* ================== CLEAR FORM ================== */
function clearForm() {
  [
    "jobTitle",
    "employer",
    "city",
    "country",
    "startDate",
    "endDate",
    "description"
  ].forEach(id => {
    if ($(id)) $(id).value = "";
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

  ul.innerHTML = "";
  text.split("\n").forEach(line => {
    if (line.trim()) {
      const li = document.createElement("li");
      li.textContent = line.trim();
      ul.appendChild(li);
    }
  });
}

/* ================== NAVIGATION ================== */
function goToStep3() {
  window.location.href = "step-3.html";
}
