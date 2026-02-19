const $ = id => document.getElementById(id);

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
/* ================= SELECTED TEMPLATE ================= */
const selectedTemplate =
  localStorage.getItem("selectedTemplate") || "academicYellow";

/* ================= LOAD TEMPLATE CSS ================= */
(function () {
  if (document.getElementById("template-style")) return;

  const link = document.createElement("link");
  link.id = "template-style";
  link.rel = "stylesheet";
  link.href = TEMPLATES[selectedTemplate].css;
  document.head.appendChild(link);
})();

/* ================= LOAD TEMPLATE HTML ================= */
const templateRes = await fetch(TEMPLATES[selectedTemplate].html);
const html = await templateRes.text();
$("resumePreview").innerHTML = html;
restore();
bindLivePreview();

/* ================= STORAGE ================= */
function save() {
  localStorage.setItem("step1", JSON.stringify(getFormData()));
}

function restore() {
  const d = JSON.parse(localStorage.getItem("step1") || "{}");

  Object.keys(getFormData()).forEach(id => {
    if ($(id)) $(id).value = d[id] || "";
  });

  updatePreview();
}

/* ================= LIVE DATA ================= */
function getFormData() {
  return {
    name: $("name").value,
    title: $("title").value,
    email: $("email").value,
    phone: $("phone").value,
    location: $("location").value,
    summary: $("summary").value,
    languages: $("languages").value,
    certs: $("certs").value
  };
}

/* ================= PREVIEW ================= */
function updatePreview() {
  const d = getFormData();

  set("previewName", d.name);
  set("previewTitle", d.title);
  set("previewEmail", d.email);
  set("previewPhone", d.phone);
  set("previewLocation", d.location);
  set("previewSummary", d.summary);

  fill("pLanguages", d.languages);
  fill("pCerts", d.certs);
}

function set(id, value) {
  const el = $(id);
  if (el) el.textContent = value || "";
}

function fill(id, text) {
  const ul = $(id);
  if (!ul) return;

  ul.innerHTML = (text || "")
    .split("\n")
    .filter(Boolean)
    .map(line => `<li>${line}</li>`)
    .join("");
}

/* ================= EVENTS ================= */
function bindLivePreview() {
  document.querySelectorAll("input, textarea").forEach(el => {
    el.addEventListener("input", () => {
      save();
      updatePreview();
    });
  });
}

$("nextBtn").onclick = () => {
  save();
  globalThis.location.href = "step-2.html";
};