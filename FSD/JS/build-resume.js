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
const templateHtml = await templateRes.text();
$("resumePreview").innerHTML = templateHtml;
loadStep1();
loadEducation();
loadExperience();
loadSkills();

/* ================== STEP 1 : HEADER ================== */
function loadStep1() {
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

/* ================== STEP 2 : EDUCATION ================== */
function loadEducation() {
  const d = JSON.parse(localStorage.getItem("step2") || "{}");
  const section = $("educationSection");

  if (!section || !d.degree) {
    section?.classList.add("hide-section");
    return;
  }

  const dateText = d.current
    ? `Expected ${formatMonth(d.month)}`
    : formatMonth(d.month);

  const detailsListItems = d.details?.length
    ? d.details.map(x => "<li>" + x + "</li>").join("")
    : "";
  const detailsHtml = detailsListItems ? "<ul>" + detailsListItems + "</ul>" : "";

  section.innerHTML = `
    <h3>EDUCATION</h3>
    <ul>
      <li>
        <strong>${d.degree} in ${d.field}</strong><br>
        ${d.school} | ${d.location}<br>
        <em>${dateText}</em>
        ${detailsHtml}
      </li>
    </ul>
  `;

  section.classList.remove("hide-section");
}

/* ================== STEP 3 : EXPERIENCE ================== */
function loadExperience() {
  const list = JSON.parse(localStorage.getItem("experiences") || "[]");
  const section = $("previewExperienceSection");
  const box = $("previewExperienceList");

  if (!section || !box || !list.length) {
    section?.classList.add("hide-section");
    return;
  }

  box.innerHTML = "";

  list.forEach(exp => {
    const div = document.createElement("div");
    div.className = "exp-item";
    div.innerHTML = `
      <strong>${exp.jobTitle} – ${exp.employer}</strong><br>
      <small>
        ${exp.city || ""}${exp.country ? ", " + exp.country : ""}
        | ${exp.startDate} – ${exp.endDate}
      </small>
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

  section.classList.remove("hide-section");
}

/* ================== STEP 4 : SKILLS ================== */
function loadSkills() {
  const skills = JSON.parse(localStorage.getItem("skills") || "[]");
  const ul = $("previewSkills");

  // ✅ SAFE GUARD
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
