/* ================== OBSERVER ================== */
const sections = document.querySelectorAll(".fade-section");

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add("show");
  });
}, { threshold: 0.15 });

sections.forEach(sec => observer.observe(sec));

/* ================== TEMPLATES ================== */
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

function getRankBadge(rank) {
  if (rank === 1) return "🏆";
  if (rank === 2) return "🥈";
  if (rank === 3) return "🥉";
  return "🔹";
}

/* ================== LOAD RESUMES ================== */
const res = await fetch("/api/resumes", { credentials: "include" });
const resumes = await res.json();
const container = document.getElementById("resumeList");

if (resumes.length) {
  container.innerHTML = resumes.map(r => `
    <div class="resume-card fade-card" data-id="${r._id}"
         onclick="openResumePreview('${r._id}')">

      <!-- ❌ DELETE BUTTON -->
      <button class="delete-resume-btn"
              onclick="deleteResume(event, '${r._id}')">✕</button>

      <!-- 📥 DOWNLOAD BUTTON -->
      <button class="download-resume-btn"
              onclick="downloadResumeDirect(event, '${r._id}')"
              title="Download Resume">
        <i class="bi bi-download"></i>
      </button>

      <div class="rank-badge">
        ${getRankBadge(r.rank)}
        Rank ${r.rank}
      </div>

      <h3>${r.title}</h3>
      <p>Score: <strong>${r.score} / 100</strong></p>
      <p>Template: ${r.template}</p>
      ${r.created_at ? `<p class="text-muted small mb-0"><i class="bi bi-calendar3 me-1"></i>${new Date(r.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>` : ''}
    </div>
  `).join("");

  container.querySelectorAll(".fade-card")
    .forEach(card => observer.observe(card));
} else {
  container.innerHTML = "<p>No resume created</p>";
}

/* ================= OPEN PREVIEW ================= */
function openResumePreview(resumeId) {
  console.log("Opening resume preview for ID:", resumeId);
  fetch(`/api/resumes/${resumeId}`, { credentials: "include" })
    .then(res => {
      console.log("API Response status:", res.status);
      return res.json();
    })
    .then(resume => {
      console.log("Received resume object:", resume);
      console.log("Resume data structure:", JSON.stringify(resume, null, 2));
      
      if (!resume?.data) {
        console.error("Resume or resume.data is missing!", resume);
        alert("Error: Resume data not found. Please try again.");
        return;
      }
      
      loadFinalTemplate(resume);

      // 🔥 set resumeId on score button
      const scoreBtn = document.querySelector(".resume-score-btn");
      if (scoreBtn) scoreBtn.dataset.id = resumeId;

      // Update modal header title
      const titleEl = document.getElementById("resumePreviewTitle");
      if (titleEl && resume.title) {
        titleEl.textContent = resume.title;
      }

      document
        .getElementById("resumePreviewOverlay")
        .classList.remove("hidden");

      document.body.style.overflow = "hidden";
    })
    .catch(err => {
      console.error("Error fetching resume:", err);
      alert("Error loading resume: " + err.message);
    });
}





function closeResumePreview() {
  document.getElementById("resumePreviewOverlay")
    .classList.add("hidden");

  document.body.style.overflow = "auto";
}



/* ================= LOAD TEMPLATE ================= */
function loadFinalTemplate(resume) {
    console.log("TEMPLATE KEY:", resume.template);
  const templateKey = resume.template || "professionalBlue";
  const tpl = TEMPLATES[templateKey];
    console.log("TEMPLATE OBJECT:", tpl);
  if (!tpl) {
    alert("Template not found. Using default template.");
    return;
  }


  const old = document.getElementById("final-template-style");
  if (old) old.remove();

  const link = document.createElement("link");
  link.id = "final-template-style";
  link.rel = "stylesheet";
  link.href = tpl.css;
  document.head.appendChild(link);

  fetch(tpl.html)
    .then(res => res.text())
    .then(html => {
      const previewContainer = document.getElementById("finalResumePreview");
      if (!previewContainer) {
        console.error("finalResumePreview container not found");
        return;
      }
      
      console.log("Loading template HTML into container");
      previewContainer.innerHTML = html;
      afterRenderAndDelay(() => injectResumeDataAndVerify(resume));
    })
    .catch(err => {
      console.error("Error loading template:", err);
      alert("Error loading template: " + err.message);
    });
}

function afterRenderAndDelay(fn, delay = 100) {
  requestAnimationFrame(() => setTimeout(fn, delay));
}

function logPreviewContent() {
  console.log("=== AFTER INJECTION ===");
  console.log("previewName content:", document.getElementById("previewName")?.textContent);
  console.log("previewTitle content:", document.getElementById("previewTitle")?.textContent);
  console.log("previewEmail content:", document.getElementById("previewEmail")?.textContent);
  console.log("previewPhone content:", document.getElementById("previewPhone")?.textContent);
  console.log("previewSkills innerHTML:", document.getElementById("previewSkills")?.innerHTML);
}

function injectResumeDataAndVerify(resume) {
  console.log("=== INJECTING DATA ===");
  console.log("Full resume object:", resume);
  console.log("Resume.data:", resume.data);
  console.log("Resume.data.step1:", resume.data?.step1);
  console.log("Resume.data.step2:", resume.data?.step2);
  console.log("Resume.data.step3:", resume.data?.step3);
  console.log("Resume.data.step4:", resume.data?.step4);
  console.log("Resume.data.customSections:", resume.data?.customSections);

  if (resume?.data) {
    console.log("Verifying template elements exist:");
    console.log("previewName exists:", !!document.getElementById("previewName"));
    console.log("previewTitle exists:", !!document.getElementById("previewTitle"));
    console.log("previewEmail exists:", !!document.getElementById("previewEmail"));
    console.log("previewPhone exists:", !!document.getElementById("previewPhone"));
    console.log("previewLocation exists:", !!document.getElementById("previewLocation"));
    console.log("previewSkills exists:", !!document.getElementById("previewSkills"));

    injectFinalData(resume.data);
    setTimeout(logPreviewContent, 100);
  } else {
    console.error("No resume data found in response");
    alert("Error: Resume data is missing. Please try creating the resume again.");
  }
}

/* ================= HELPERS ================= */
function setText(id, value) {
  const el = document.getElementById(id);
  if (el) {
    // Set text even if value is empty string, null, or undefined (to clear fields)
    const textValue = value == null ? "" : String(value);
    el.textContent = textValue;
    
    // Ensure element is visible if it has content
    if (textValue.trim()) {
      el.style.display = "";
      el.classList.remove("hide-section");
    }
  }
}

function fillList(id, text) {
  const ul = document.getElementById(id);
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
function loadSkills() {
  const skills = JSON.parse(localStorage.getItem("skills") || "[]");

  const ul = document.getElementById("previewSkills");
  const section = ul?.closest("section");

  if (!ul || !skills.length) {
    section?.classList.add("hide-section");
    return;
  }

  ul.innerHTML = "";
  skills.forEach(skill => {
    const li = document.createElement("li");
    li.textContent = skill;
    ul.appendChild(li);
  });

  // ✅ IMPORTANT
  section.classList.remove("hide-section");
}

/* ================= DOWNLOAD PDF (STABLE) ================= */
function downloadResumePDF() {
  const element = document.getElementById("finalResumePreview");

  setTimeout(() => {
    html2pdf()
      .set({
        margin: 5,
        filename: "resume.pdf",
        image: { type: "jpeg", quality: 1 },
        html2canvas: { scale: 2, useCORS: true, scrollY: 0 },
        jsPDF: { unit: "mm", format: "a4", orientation: "portrait" }
      })
      .from(element)
      .save();
  }, 300);
}

/* ================= DOWNLOAD RESUME DIRECTLY FROM CARD ================= */
function onTemplateHtmlLoaded(html, resume, tempContainer, cleanup) {
  tempContainer.innerHTML = html;
  afterRenderAndDelay(() => prepareTempContainerAndInject(resume, tempContainer, cleanup), 200);
}

function prepareTempContainerAndInject(resume, tempContainer, cleanup) {
  const originalFinalPreview = document.getElementById("finalResumePreview");
  if (originalFinalPreview?.id === "finalResumePreview") {
    originalFinalPreview.id = "originalFinalResumePreviewBackup";
  }

  const finalPreviewWrapper = document.createElement("div");
  finalPreviewWrapper.id = "finalResumePreview";

  const resumeContent = tempContainer.querySelector(".resume");
  if (resumeContent) {
    finalPreviewWrapper.appendChild(resumeContent);
  } else {
    Array.from(tempContainer.children).forEach(child => {
      finalPreviewWrapper.appendChild(child);
    });
  }

  tempContainer.appendChild(finalPreviewWrapper);
  injectFinalData(resume.data);
  setTimeout(() => generatePdfFromResumeElement(tempContainer, finalPreviewWrapper, resume, cleanup), 1000);
}

function generatePdfFromResumeElement(tempContainer, finalPreviewWrapper, resume, cleanup) {
  const resumeElement = tempContainer.querySelector(".resume") ||
    finalPreviewWrapper.querySelector(".resume") ||
    finalPreviewWrapper.firstElementChild ||
    tempContainer.firstElementChild;

  if (!resumeElement?.innerHTML?.trim()) {
    console.error("Resume element not found or empty in temp container");
    console.log("Temp container HTML:", tempContainer.innerHTML.substring(0, 500));
    console.log("FinalPreviewWrapper HTML:", finalPreviewWrapper.innerHTML.substring(0, 500));
    alert("Error: Could not generate PDF. Content is empty.");
    cleanup();
    return;
  }

  console.log("Generating PDF from element:", resumeElement);
  console.log("Element has content:", resumeElement.innerHTML.length > 0);
  console.log("Element classes:", resumeElement.className);

  const resumeWidth = 800;
  resumeElement.style.width = resumeWidth + "px";
  resumeElement.style.maxWidth = resumeWidth + "px";
  resumeElement.style.boxSizing = "border-box";

  const style = document.createElement("style");
  style.id = "pdf-page-break-style";
  style.textContent = `
    .resume, .resume * {
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
    section, .main-section, .content-card, .card-content {
      page-break-inside: avoid !important;
      break-inside: avoid !important;
    }
  `;
  document.head.appendChild(style);

  const forcedHeight = resumeElement.offsetHeight; // Force layout recalculation
  const actualHeight = Math.max(resumeElement.scrollHeight, forcedHeight);
  const a4HeightPx = 1123;
  const a4WidthPx = 794;
  const heightScale = actualHeight > a4HeightPx ? a4HeightPx / actualHeight : 1;
  const widthScale = resumeWidth > a4WidthPx ? a4WidthPx / resumeWidth : 1;
  const finalScale = Math.min(heightScale, widthScale, 1);

  console.log("Resume element dimensions:", {
    width: resumeElement.offsetWidth,
    height: actualHeight,
    scrollHeight: resumeElement.scrollHeight,
    a4Height: a4HeightPx,
    heightScale,
    widthScale,
    finalScale
  });

  html2pdf()
    .set({
      margin: [0, 0, 0, 0],
      filename: `${(resume.title || "resume").replaceAll(/[^a-z0-9]/gi, "_")}.pdf`,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: {
        scale: 2 * finalScale,
        useCORS: true,
        scrollY: 0,
        logging: false,
        windowWidth: resumeWidth,
        width: resumeWidth,
        height: actualHeight,
        allowTaint: false,
        backgroundColor: "#ffffff",
        x: 0,
        y: 0,
        removeContainer: true
      },
      jsPDF: {
        unit: "mm",
        format: "a4",
        orientation: "portrait",
        compress: true
      },
      pagebreak: { mode: ["avoid-all", "css", "legacy"] }
    })
    .from(resumeElement)
    .save()
    .then(() => {
      const pdfStyle = document.getElementById("pdf-page-break-style");
      if (pdfStyle) {
        pdfStyle.remove();
      }
    })
    .then(() => {
      console.log("✅ Resume downloaded successfully");
      cleanup();
    })
    .catch(err => {
      console.error("Error generating PDF:", err);
      alert("Error generating PDF: " + err.message);
      cleanup();
    });
}

function downloadResumeDirect(event, resumeId) {
  // Prevent the card click event from firing
  event.stopPropagation();
  
  // Show loading indicator
  const btn = event.target.closest('.download-resume-btn');
  const originalHTML = btn.innerHTML;
  btn.innerHTML = '<i class="bi bi-hourglass-split"></i>';
  btn.disabled = true;
  
  console.log("Downloading resume:", resumeId);
  
  // Fetch resume data
  fetch(`/api/resumes/${resumeId}`, { credentials: "include" })
    .then(res => res.json())
    .then(resume => {
      if (!resume?.data) {
        alert("Error: Resume data not found.");
        btn.innerHTML = originalHTML;
        btn.disabled = false;
        return;
      }
      
      // Load the template into a hidden container
      const tpl = TEMPLATES[resume.template] || TEMPLATES.academicYellow;
      
      // Create a temporary container for PDF generation
      // Position it completely off-screen to prevent any visual flash
      const tempContainer = document.createElement("div");
      tempContainer.id = "tempResumePreview";
      tempContainer.style.position = "absolute";
      tempContainer.style.left = "-10000px";
      tempContainer.style.top = "0";
      tempContainer.style.width = "800px";
      tempContainer.style.height = "auto";
      tempContainer.style.overflow = "visible";
      tempContainer.style.visibility = "hidden";
      tempContainer.style.pointerEvents = "none";
      document.body.appendChild(tempContainer);
      
      // Check if CSS is already loaded
      const existingCSS = document.querySelector(`link[href="${tpl.css}"]`);
      let cssLink = existingCSS;
      
      if (!existingCSS) {
        // Load CSS
        cssLink = document.createElement("link");
        cssLink.rel = "stylesheet";
        cssLink.href = tpl.css;
        cssLink.id = "temp-resume-css";
        document.head.appendChild(cssLink);
      }
      
      // Wait for CSS to load if it's new
      const loadTemplate = () => {
        // Load HTML template
        fetch(tpl.html)
          .then(res => res.text())
          .then(html => onTemplateHtmlLoaded(html, resume, tempContainer, cleanup))
          .catch(err => {
            console.error("Error loading template:", err);
            alert("Error loading template. Please try again.");
            cleanup();
          });
      };
      
      // Cleanup function
      const cleanup = () => {
        try {
          // Restore original finalResumePreview if it was swapped
          const backup = document.getElementById("originalFinalResumePreviewBackup");
          if (backup) {
            backup.id = "finalResumePreview";
          }
          
          // Remove temporary container
          const temp = document.getElementById("tempResumePreview");
          if (temp) {
            temp.remove();
          }
          
          // Remove temporary CSS if we added it
          if (!existingCSS && cssLink?.parentNode) {
            cssLink.remove();
          }
        } catch (e) {
          console.error("Cleanup error:", e);
        }
        btn.innerHTML = originalHTML;
        btn.disabled = false;
      };
      
      // If CSS is new, wait for it to load
      if (!existingCSS && cssLink) {
        cssLink.onload = loadTemplate;
        cssLink.onerror = () => {
          console.error("Error loading CSS");
          loadTemplate(); // Try anyway
        };
        // Fallback timeout
        setTimeout(() => {
          if (btn.disabled) {
            loadTemplate();
          }
        }, 3000);
      } else {
        loadTemplate();
      }
    })
    .catch(err => {
      console.error("Error fetching resume:", err);
      alert("Error loading resume. Please try again.");
      btn.innerHTML = originalHTML;
      btn.disabled = false;
    });
}
/* ================= RESUME SCORE BUTTON ================= */
document.addEventListener("click", async (e) => {
  if (!e.target.classList.contains("resume-score-btn")) return;

  const resumeId = e.target.dataset.id;
  console.log("Resume ID:", resumeId); // 🔥 debug

  const res = await fetch(`/api/resumes/score/${resumeId}`);
  const data = await res.json();

  const finalScoreEl = document.getElementById("finalScore");
  if (finalScoreEl) finalScoreEl.innerText = `${data.score} / 100`;

  const list = document.getElementById("scoreList");
  if (list) {
    list.innerHTML = "";
    for (let key in data.breakdown) {
      list.innerHTML += `
        <li class="list-group-item d-flex justify-content-between bg-transparent border-secondary text-white">
          <span>${key}</span>
          <strong>${data.breakdown[key]}</strong>
        </li>
      `;
    }
  }

  const warningsEl = document.getElementById("scoreWarnings");
  if (warningsEl && data.warnings && data.warnings.length > 0) {
    warningsEl.style.display = "block";
    warningsEl.innerHTML = "<strong>Please fix:</strong><ul class=\"mb-0 mt-1\">" +
      data.warnings.map(function (w) { return "<li>" + w + "</li>"; }).join("") + "</ul>";
  } else if (warningsEl) {
    warningsEl.style.display = "none";
    warningsEl.innerHTML = "";
  }

  const modalEl = document.getElementById("resumeScoreModal");
  if (modalEl) bootstrap.Modal.getOrCreateInstance(modalEl).show();
});
/* ================= CLOSE PREVIEW BUTTON ================= */
document.addEventListener("click", (e) => {
  if (e.target.closest("#closePreview")) {
    const overlay = document.getElementById("resumePreviewOverlay");
    if (overlay) {
      overlay.classList.add("hidden");
      document.body.style.overflow = "auto";
    }
  }
});

const skillsRes = await fetch("/api/resumes/skills/frequency");
const skillsData = await skillsRes.json();
const topSkillsContainer = document.getElementById("topSkills");
if (topSkillsContainer) {
  topSkillsContainer.innerHTML = "";

  const entries = Object.entries(skillsData)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6); // show top 6 skills

  if (entries.length === 0) {
    topSkillsContainer.innerHTML = "<p class='text-muted'>No skills data available</p>";
  } else {
    const maxCount = entries[0][1];

    entries.forEach(([skill, count]) => {
      const percent = Math.round((count / maxCount) * 100);

      topSkillsContainer.innerHTML += `
        <div class="skill-row">
          <span class="skill-name">${skill}</span>

          <div class="skill-bar">
            <div class="skill-bar-fill" style="width:${percent}%"></div>
          </div>

          <span class="skill-count">${count}</span>
        </div>
      `;
    });
  }
}

async function deleteResume(event, resumeId) {
  event.stopPropagation(); // 🔥 prevents opening preview

  if (!confirm("Delete this resume permanently?")) return;

  try {
    const res = await fetch(`/api/resumes/${resumeId}`, {
      method: "DELETE",
      credentials: "include"
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.message || "Failed to delete resume");
      return;
    }

    // ✅ remove card from UI
    document
      .querySelector(`.resume-card[data-id="${resumeId}"]`)
      ?.remove();

  } catch (err) {
    console.error(err);
    alert("Server error while deleting resume");
  }
}


// Auto-populate form with sample data
function autoPopulateAIForm() {
  // Basic Details
  document.getElementById("aiName").value = "John Doe";
  document.getElementById("aiTitle").value = "Software Engineer";
  document.getElementById("aiEmail").value = "john.doe@email.com";
  document.getElementById("aiPhone").value = "+1 (555) 123-4567";
  document.getElementById("aiLocation").value = "San Francisco, CA";
  document.getElementById("aiSummary").value = "Experienced software engineer with 5+ years of expertise in full-stack development, cloud architecture, and agile methodologies. Passionate about building scalable applications and leading cross-functional teams.";

  // Additional Details
  document.getElementById("aiLanguages").value = "English\nSpanish\nFrench";
  document.getElementById("aiCertificates").value = "AWS Certified Solutions Architect\nGoogle Cloud Professional\nCertified Kubernetes Administrator";
  document.getElementById("aiJD").value = "We are looking for a skilled Software Engineer to join our team. The ideal candidate should have experience with modern web technologies, cloud platforms, and software development best practices.";

  // Education
  document.getElementById("aiSchool").value = "Stanford University";
  document.getElementById("aiDegree").value = "Bachelor of Science";
  document.getElementById("aiField").value = "Computer Science";
  document.getElementById("aiGradYear").value = "2019";

  // Experience Level
  document.getElementById("aiExperience").value = "experienced";
  
  // Show experience section
  const expSection = document.getElementById("aiExperienceSection");
  if (expSection) {
    expSection.classList.remove("d-none");
    
    // Clear existing experience blocks
    const container = document.getElementById("experienceContainer");
    if (container) {
      container.innerHTML = "";
      
      // Add sample experience entries
      const sampleExperiences = [
        {
          jobTitle: "Senior Software Engineer",
          employer: "Tech Corp Inc.",
          city: "San Francisco",
          country: "USA",
          startMonth: "2021-01",
          endMonth: "2024-12",
          description: "Led development of microservices architecture serving 1M+ users. Implemented CI/CD pipelines reducing deployment time by 60%. Mentored junior developers and conducted code reviews."
        },
        {
          jobTitle: "Software Engineer",
          employer: "StartupXYZ",
          city: "Palo Alto",
          country: "USA",
          startMonth: "2019-06",
          endMonth: "2020-12",
          description: "Developed RESTful APIs using Node.js and Express. Built responsive frontend components with React. Collaborated with product team to deliver features on time."
        }
      ];
      
      sampleExperiences.forEach(exp => {
        // Use the template structure to match the existing format
        const template = document.getElementById("experienceTemplate");
        if (template) {
          const clone = template.content.cloneNode(true);
          const block = clone.querySelector(".experience-block");
          
          // Populate the cloned template with sample data
          block.querySelector(".exp-title").value = exp.jobTitle;
          block.querySelector(".exp-employer").value = exp.employer;
          block.querySelector(".exp-city").value = exp.city;
          block.querySelector(".exp-country").value = exp.country;
          block.querySelector(".exp-start").value = exp.startMonth;
          block.querySelector(".exp-end").value = exp.endMonth;
          block.querySelector(".exp-desc").value = exp.description;
          
          container.appendChild(clone);
        } else {
          // Fallback if template not found
          const block = document.createElement("div");
          block.className = "experience-block border p-3 mt-3";
          block.innerHTML = `
            <input class="form-control mb-2 exp-title" placeholder="Job Title" value="${exp.jobTitle}">
            <input class="form-control mb-2 exp-employer" placeholder="Employer" value="${exp.employer}">
            <div class="row">
              <div class="col">
                <input class="form-control mb-2 exp-city" placeholder="City" value="${exp.city}">
              </div>
              <div class="col">
                <input class="form-control mb-2 exp-country" placeholder="Country" value="${exp.country}">
              </div>
            </div>
            <div class="row">
              <div class="col">
                <input type="month" class="form-control mb-2 exp-start" value="${exp.startMonth}">
              </div>
              <div class="col">
                <input type="month" class="form-control mb-2 exp-end" value="${exp.endMonth}">
              </div>
            </div>
            <textarea class="form-control exp-desc" placeholder="Job Description">${exp.description}</textarea>
          `;
          container.appendChild(block);
        }
      });
    }
  }

  // Skills
  const skillsField = document.getElementById("skillsField");
  if (skillsField) {
    skillsField.classList.remove("d-none");
    document.getElementById("aiSkills").value = "JavaScript\nPython\nReact\nNode.js\nAWS\nDocker\nKubernetes\nMongoDB\nPostgreSQL\nGit";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const aiBtn = document.getElementById("aiCreateBtn");
  const aiModal = document.getElementById("aiResumeModal");

  if (!aiBtn || !aiModal) {
    console.error("AI button or modal not found");
    return;
  }

  aiBtn.addEventListener("click", async () => {
    try {
      showAIStep1();
      bootstrap.Modal.getOrCreateInstance(aiModal).show();
    } catch (err) {
      console.error("AI modal error:", err);
      alert("Unable to open AI resume builder");
    }
  });

  document.getElementById("aiContinueBtn")?.addEventListener("click", function () { proceedFromRoleToForm(); });
  document.getElementById("aiBackBtn")?.addEventListener("click", function () { showAIStep1(); });
});

function showAIStep1() {
  document.getElementById("aiStep1").style.display = "block";
  document.getElementById("aiStep2").style.display = "none";
  document.getElementById("aiStep1Footer").style.display = "inline";
  document.getElementById("aiStep2Footer").style.display = "none";
  document.getElementById("aiTargetRole").value = "";

  // Clear personal info so "Back" doesn't keep old values
  const idsToClear = ["aiName", "aiEmail", "aiPhone", "aiLocation"];
  idsToClear.forEach(function (id) {
    const el = document.getElementById(id);
    if (el) el.value = "";
  });

  document.getElementById("aiTargetRole").focus();
}

function showAIStep2() {
  document.getElementById("aiStep1").style.display = "none";
  document.getElementById("aiStep2").style.display = "block";
  document.getElementById("aiStep1Footer").style.display = "none";
  document.getElementById("aiStep2Footer").style.display = "inline";
}

async function proceedFromRoleToForm() {
  const roleInput = document.getElementById("aiTargetRole");
  const role = roleInput?.value?.trim() || "";
  if (!role) {
    alert("Please enter the role you want (e.g. Java Developer, Data Scientist).");
    return;
  }
  const btn = document.getElementById("aiContinueBtn");
  const originalText = btn ? btn.innerHTML : "";
  if (btn) { btn.disabled = true; btn.innerHTML = "<span class=\"spinner-border spinner-border-sm me-2\"></span>Generating..."; }
  try {
    const res = await fetch("/ai/suggest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ role: role })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to get suggestions");

    document.getElementById("aiTitle").value = data.title || role;
    document.getElementById("aiSummary").value = data.summary || "";
    document.getElementById("aiJD").value = data.job_description || "";
    const skillsEl = document.getElementById("aiSkills");
    if (skillsEl) skillsEl.value = Array.isArray(data.skills) ? data.skills.join("\n") : (data.skills || "");

    document.getElementById("aiExperience").value = "fresher";
    const expSection = document.getElementById("aiExperienceSection");
    if (expSection) expSection.classList.add("d-none");
    const expContainer = document.getElementById("experienceContainer");
    if (expContainer) expContainer.innerHTML = "";

    showAIStep2();
  } catch (err) {
    console.error(err);
    alert(err.message || "Could not generate suggestions. You can still fill the form manually.");
    document.getElementById("aiTitle").value = role;
    showAIStep2();
  } finally {
    if (btn) { btn.disabled = false; btn.innerHTML = originalText; }
  }
}

async function submitAIResume() {
  const role = document.getElementById("aiTitle").value.trim();
  const jd = document.getElementById("aiJD").value.trim();
  const exp = document.getElementById("aiExperience").value;
  let experience = [];

    if (document.getElementById("aiExperience").value === "experienced") {
      document.querySelectorAll(".experience-block").forEach(block => {
      const jobTitle = block.querySelector(".exp-title").value.trim();
      if (!jobTitle) return;

      experience.push({
        jobTitle,
        employer: block.querySelector(".exp-employer").value,
        city: block.querySelector(".exp-city").value,
        country: block.querySelector(".exp-country").value,
        startMonth: block.querySelector(".exp-start").value,
        endMonth: block.querySelector(".exp-end").value,
        description: block.querySelector(".exp-desc").value
      });
    });
    }


  if (!role) {
    alert("Please enter a role");
    return;
  }

  try {
    const res = await fetch("/ai/create-resume", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
          role,
          job_description: jd,
          experience_level: exp,
          template: "blueCorporate", // Auto-select blueCorporate template

          personal: {
              name: document.getElementById("aiName").value || "",
              title: document.getElementById("aiTitle").value || "",
              email: document.getElementById("aiEmail").value || "",
              phone: document.getElementById("aiPhone").value || "",
              location: document.getElementById("aiLocation").value || "",
              summary: document.getElementById("aiSummary").value,

              languages: document
                .getElementById("aiLanguages")
                ?.value.split("\n")
                .filter(Boolean) || [],

              certificates: document
                .getElementById("aiCertificates")
                ?.value.split("\n")
                .filter(Boolean) || []
            },

          education: {
            institution: document.getElementById("aiSchool").value,
            degree: document.getElementById("aiDegree").value,
            field: document.getElementById("aiField").value,
            year: document.getElementById("aiGradYear").value
          },

          experience: experience,

          skills: document
            .getElementById("aiSkills")
            .value
            .split("\n")
            .filter(Boolean)
        })
    });

    const raw = await res.text();
    console.log("AI RAW RESPONSE:", raw);

    if (!res.ok) {
      throw new Error(raw);
    }

    const data = JSON.parse(raw);

    bootstrap.Modal.getInstance(
      document.getElementById("aiResumeModal")
    ).hide();

    openResumePreview(data.resumeId);

  }catch (e) {
      console.error("AI ERROR:", e);
      alert("AI resume creation failed:\n" + e.message);
    }

}

function _injectGetEl(container, id) {
  return container ? container.querySelector("#" + id) : document.getElementById(id);
}

function _injectSetText(container, id, value) {
  const el = _injectGetEl(container, id);
  if (el) {
    el.textContent = value == null ? "" : String(value);
    if ((value == null ? "" : String(value)).trim()) el.style.display = "";
  }
}

function _injectBasicInfo(container, data) {
  if (!data.step1) return;
  const step1 = data.step1;
  const name = (step1.name || "").trim();
  const title = (step1.title || "").trim();
  const email = (step1.email || "").trim();
  const phone = (step1.phone || "").trim();
  const location = (step1.location || "").trim();
  const fields = [
    ["previewName", name],
    ["previewTitle", title],
    ["previewEmail", email],
    ["previewPhone", phone],
    ["previewLocation", location]
  ];
  fields.forEach(([id, val]) => {
    const el = _injectGetEl(container, id);
    if (el) {
      el.textContent = val;
      el.style.display = val ? "" : "none";
    }
  });
}

function _injectSkillsList(data) {
  if (Array.isArray(data.step4)) {
    return data.step4.map(s => (typeof s === "string" ? s : s?.name)).filter(Boolean);
  }
  if (typeof data.step4 === "string" && data.step4.trim()) {
    return data.step4.split("\n").map(s => s.trim()).filter(Boolean);
  }
  return [];
}

function _injectSkills(container, data) {
  const skills = _injectSkillsList(data);
  const skillsBox = _injectGetEl(container, "previewSkills");
  const skillsSection = _injectGetEl(container, "skillsSection");
  if (!skillsBox) {
    console.error("previewSkills element not found!");
    return;
  }
  console.log("Setting skills:", skills);
  if (skills.length) {
    skillsBox.innerHTML = skills.map(s => `<li>${s}</li>`).join("");
    skillsBox.style.display = "";
    revealSection(skillsBox);
    skillsSection?.classList.remove("hide-section");
    skillsSection?.style.setProperty("display", "");
  } else {
    skillsBox.innerHTML = "";
    skillsBox.style.display = "none";
    skillsSection?.classList.add("hide-section");
    skillsSection?.style.setProperty("display", "none");
  }
}

function _injectSummary(container, data, skills) {
  const summaryEl = _injectGetEl(container, "previewSummary");
  if (!summaryEl) return;
  const summary = (data.step1?.summary || "").trim();
  summaryEl.innerHTML = summary ? highlightKeywords(summary, skills) : "";
  summaryEl.style.display = summary ? "" : "none";
  if (summary) revealSection(summaryEl);
}

function _injectLanguages(container, data) {
  const langList = _injectGetEl(container, "pLanguages");
  if (!langList) return;
  let languages = [];
  if (data.step1) {
    if (Array.isArray(data.step1.languages)) languages = data.step1.languages;
    else if (typeof data.step1.languages === "string" && data.step1.languages.trim()) {
      languages = data.step1.languages.split("\n").map(l => l.trim()).filter(Boolean);
    }
  }
  langList.innerHTML = languages.length ? languages.map(l => `<li>${l}</li>`).join("") : "";
  langList.style.display = languages.length ? "" : "none";
  if (languages.length) revealSection(langList);
}

function _injectCertifications(container, data) {
  const certList = _injectGetEl(container, "pCerts");
  if (!certList) return;
  let certificates = [];
  if (data.step1) {
    const certData = data.step1.certificates || data.step1.certs;
    if (Array.isArray(certData)) certificates = certData;
    else if (typeof certData === "string" && certData.trim()) {
      certificates = certData.split("\n").map(c => c.trim()).filter(Boolean);
    }
  }
  certList.innerHTML = certificates.length ? certificates.map(c => `<li>${c}</li>`).join("") : "";
  certList.style.display = certificates.length ? "" : "none";
  if (certificates.length) revealSection(certList);
}

function _formatGraduationDate(s2) {
  if (s2.month) return s2.current ? `Expected ${formatMonth(s2.month)}` : formatMonth(s2.month);
  if (s2.year) return (s2.year || "").toString().trim();
  return "";
}

function _applyEducationSectionVisibility(container, edu, degree, field, school, location) {
  const hasContent = degree || field || school;
  edu.classList.toggle("hide-section", !hasContent);
  edu.classList.toggle("show", !!hasContent);
  edu.style.display = hasContent ? "" : "none";
  if (hasContent) {
    if (degree) _injectGetEl(container, "previewDegree")?.style.setProperty("display", "", "important");
    if (field) _injectGetEl(container, "previewField")?.style.setProperty("display", "", "important");
    if (school) _injectGetEl(container, "previewEduInstitute")?.style.setProperty("display", "", "important");
    if (location) _injectGetEl(container, "previewEduLocation")?.style.setProperty("display", "", "important");
  }
}

function _injectEducation(container, data) {
  if (!data.step2) return;
  const s2 = data.step2;
  const degree = (s2.degree || "").trim();
  const field = (s2.field || "").trim();
  const school = (s2.school || s2.institution || "").trim();
  const location = (s2.location || "").trim();
  _injectSetText(container, "previewDegree", degree);
  _injectSetText(container, "previewField", field);
  _injectSetText(container, "previewEduInstitute", school);
  _injectSetText(container, "previewEduLocation", location);
  _injectSetText(container, "previewGraduation", _formatGraduationDate(s2));

  const eduDetailsEl = _injectGetEl(container, "previewEduDetails");
  const hasDetails = Array.isArray(s2.details) && s2.details.length > 0;
  if (eduDetailsEl && hasDetails) {
    eduDetailsEl.innerHTML = s2.details.map(d => `<li>${d}</li>`).join("");
    eduDetailsEl.style.display = "";
  }

  const edu = _injectGetEl(container, "educationSection");
  if (edu) _applyEducationSectionVisibility(container, edu, degree, field, school, location);
}

function _injectExperience(container, data) {
  const hasExp = Array.isArray(data.step3) && data.step3.length;
  const sec = _injectGetEl(container, "previewExperienceSection");
  if (!sec) return;
  if (hasExp) {
    const list = _injectGetEl(container, "previewExperienceList");
    if (!list) return;
    list.innerHTML = data.step3.map(exp => {
      const jobTitle = exp.jobTitle || "";
      const employer = exp.employer || "";
      const city = exp.city || "";
      const country = exp.country || "";
      const startDate = exp.startMonth || exp.startDate || "";
      const endDate = exp.endMonth || exp.endDate || "";
      const description = exp.description || "";
      const listItems = description.split("\n").filter(Boolean).map(d => "<li>" + d + "</li>").join("");
      const descHtml = description.includes("\n") ? "<ul>" + listItems + "</ul>" : "<p>" + description + "</p>";
      const cityCountrySep = city && country ? ", " : "";
      const locationLine = (city || country) ? `<small>${city}${cityCountrySep}${country}</small><br>` : "";
      const dateRange = endDate ? " – " + endDate : "";
      const dateLine = (startDate || endDate) ? `<small>${startDate}${dateRange}</small>` : "";
      return `
          <div class="mb-3">
            <strong>${jobTitle}${employer ? " – " + employer : ""}</strong><br>
            ${locationLine}
            ${dateLine}
            ${descHtml}
          </div>
        `;
    }).join("");
    sec.classList.remove("hide-section");
    sec.classList.add("show");
    sec.style.display = "";
  } else {
    sec.classList.add("hide-section");
    sec.style.display = "none";
  }
}

function _injectCustomSections(container, data) {
  const customSections = data.customSections || [];
  const root = container || document;
  root.querySelectorAll(".custom-section-final").forEach(el => el.remove());
  if (!customSections.length) return;
  let rightPanel = container?.querySelector(".content-column") ?? document.querySelector(".content-column");
  rightPanel = rightPanel ?? container?.querySelector(".right-panel") ?? document.querySelector(".right-panel");
  rightPanel = rightPanel ?? container?.querySelector("main") ?? document.querySelector("main");
  rightPanel = rightPanel ?? document.querySelector("#previewExperienceSection")?.parentElement ?? document.querySelector("#educationSection")?.parentElement;
  if (!rightPanel) {
    console.error("❌ Right panel not found! Cannot add custom sections.");
    return;
  }
  const existingSection = rightPanel.querySelector(".content-card") || rightPanel.querySelector(".main-section") || rightPanel.querySelector(".card-content") || rightPanel.querySelector("section");
  let sectionClass = "main-section";
  let useWrapper = false;
  let wrapperClass = "";
  if (existingSection?.classList.contains("content-card")) {
    sectionClass = "content-card";
  } else if (existingSection?.classList.contains("card-content")) {
    sectionClass = "main-section card-content";
    useWrapper = true;
    wrapperClass = "content-box";
  }
  customSections.forEach((section, index) => {
    const sectionEl = document.createElement("section");
    sectionEl.className = `${sectionClass} custom-section-final`;
    sectionEl.id = `customSectionFinal${index}`;
    const customListItems = section.description.split("\n").filter(Boolean).map(d => "<li>" + escapeHtml(d) + "</li>").join("");
    const descHtml = section.description.includes("\n") ? "<ul>" + customListItems + "</ul>" : "<p>" + escapeHtml(section.description) + "</p>";
    sectionEl.innerHTML = useWrapper && wrapperClass
      ? `<div class="section-title"><span class="title-icon"></span><h3>${escapeHtml(section.name.toUpperCase())}</h3></div><div class="${wrapperClass}">${descHtml}</div>`
      : `<h3>${escapeHtml(section.name.toUpperCase())}</h3>${descHtml}`;
    const experienceSection = rightPanel.querySelector("#previewExperienceSection");
    if (experienceSection) {
      experienceSection.after(sectionEl);
    } else {
      const allSections = rightPanel.querySelectorAll("section");
      const lastSection = allSections[allSections.length - 1];
      if (lastSection) lastSection.after(sectionEl);
      else rightPanel.appendChild(sectionEl);
    }
    sectionEl.classList.remove("hide-section");
    sectionEl.style.display = sectionClass === "content-card" ? "block" : "";
    sectionEl.style.visibility = "visible";
  });
}

function injectFinalData(data) {
  if (!data) {
    console.warn("No resume data found, trying localStorage fallback");
    data = {
      step1: JSON.parse(localStorage.getItem("step1") || "{}"),
      step2: JSON.parse(localStorage.getItem("step2") || "{}"),
      step3: JSON.parse(localStorage.getItem("experiences") || "[]"),
      step4: JSON.parse(localStorage.getItem("skills") || "[]"),
      customSections: JSON.parse(localStorage.getItem("customSections") || "[]")
    };
  }
  if (!data.step1) console.warn("No step1 data found in resume data:", data);

  const container = document.getElementById("finalResumePreview");
  _injectBasicInfo(container, data);
  const skills = _injectSkillsList(data);
  _injectSkills(container, data);
  _injectSummary(container, data, skills);
  _injectLanguages(container, data);
  _injectCertifications(container, data);
  _injectEducation(container, data);
  _injectExperience(container, data);
  _injectCustomSections(container, data);
}


function revealSection(el) {
  if (!el) {
    console.warn("revealSection called with null element");
    return;
  }

  // Ensure the element itself is visible
  el.style.display = "";
  el.style.visibility = "visible";
  el.classList.remove("hide-section");

  // try common wrappers used by templates
  const wrapper =
    el.closest(".fade-section") ||
    el.closest("section") ||
    el.parentElement;

  if (wrapper) {
    wrapper.classList.remove("hide-section");
    wrapper.classList.add("show");
    wrapper.style.display = "";
    wrapper.style.visibility = "visible";
    console.log("Revealed section:", wrapper);
  }
}





function highlightKeywords(text, keywords) {
  if (!text || !Array.isArray(keywords)) return text;

  const escaped = keywords.map(k =>
    k.replaceAll(/[.*+?^${}()|[\]\\]/g, String.raw`\$&`)
  );

  const regex = new RegExp(String.raw`\b(${escaped.join("|")})\b`, "gi");

  return text.replace(regex, `<span class="ats-highlight">$1</span>`);
}

const expSelect = document.getElementById("aiExperience");
if (expSelect) {
  expSelect.addEventListener("change", e => {
    const section = document.getElementById("aiExperienceSection");
    section.classList.toggle("d-none", e.target.value !== "experienced");
  });
}


function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function addExperienceField() {
  const tpl = document.getElementById("experienceTemplate");
  const clone = tpl.content.cloneNode(true);
  document.getElementById("experienceContainer").appendChild(clone);
}

/* ================= ATS RESUME SCORE CHECKER ================= */

// Load saved resumes into dropdown when modal opens
document.getElementById("atsCheckModal")?.addEventListener("show.bs.modal", async function() {
  const select = document.getElementById("savedResumeSelect");
  if (!select) return;
  
  select.innerHTML = '<option value="">Loading resumes...</option>';
  
  try {
    const response = await fetch("/api/resumes/", { credentials: "include" });
    const resumes = await response.json();
    
    if (resumes && resumes.length > 0) {
      select.innerHTML = '<option value="">Select a resume...</option>';
      resumes.forEach(resume => {
        const option = document.createElement("option");
        option.value = resume._id;
        
        // Format display text with template and date for easy identification
        let displayText = resume.title || "Untitled Resume";
        
        // Add template name if available
        if (resume.template) {
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
          const templateDisplay = templateNames[resume.template] || resume.template;
          
          // Format date if available
          let dateInfo = "";
          if (resume.created_at) {
            try {
              const date = new Date(resume.created_at);
              dateInfo = ` • ${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
            } catch {
              dateInfo = ""; // Fallback when date parsing fails
            }
          }
          
          // Show: "Title [Template] • Date"
          displayText = `${displayText} [${templateDisplay}]${dateInfo}`;
        }
        
        option.textContent = displayText;
        option.title = displayText; // Tooltip for full text
        select.appendChild(option);
      });
    } else {
      select.innerHTML = '<option value="">No saved resumes found</option>';
    }
  } catch (error) {
    console.error("Error loading resumes:", error);
    select.innerHTML = '<option value="">Error loading resumes</option>';
  }
});

document.getElementById("atsCheckForm")?.addEventListener("submit", async function(e) {
  e.preventDefault();

  const checkBtn = document.getElementById("checkAtsBtn");
  const resultsDiv = document.getElementById("atsResults");
  const jobDescTextarea = document.getElementById("jobDescription");
  
  // Validate job description
  if (!jobDescTextarea.value.trim()) {
    alert("Please paste the job description.");
    return;
  }
  
  // Validate resume selection
  const resumeId = document.getElementById("savedResumeSelect").value;
  if (!resumeId) {
    alert("Please select a saved resume.");
    return;
  }
  
  // Show loading state
  const originalBtnText = checkBtn.innerHTML;
  checkBtn.disabled = true;
  checkBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Analyzing...';
  resultsDiv.style.display = "none";
  
  try {
    // Use saved resume method
    const response = await fetch("/api/ats/check-from-resume", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        resume_id: resumeId,
        job_description: jobDescTextarea.value.trim()
      }),
      credentials: "include"
    });
    
    const data = await response.json();
    
    console.log("ATS Check Response:", data);
    console.log("ATS Score received:", data.ats_score);
    console.log("Keyword Match:", data.keyword_match_percent);
    console.log("Structure Score:", data.structure_score);
    console.log("Formatting Score:", data.formatting_score);
    
    if (!response.ok || data.error) {
      throw new Error(data.error || "Failed to analyze resume");
    }
    
    // Verify score is valid
    if (data.ats_score === undefined || data.ats_score === null) {
      console.error("ATS score is missing from response:", data);
      throw new Error("Invalid response: ATS score not found");
    }
    
    // Display results
    displayATSResults(data);
    resultsDiv.style.display = "block";
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: "smooth", block: "start" });
    
  } catch (error) {
    console.error("ATS Check Error:", error);
    alert("Error analyzing resume:\n\n" + error.message);
  } finally {
    // Reset button
    checkBtn.disabled = false;
    checkBtn.innerHTML = originalBtnText;
  }
});

function _atsNormalizeScore(data) {
  const raw = data.resume_score ?? data.ats_score;
  if (raw == null) return 0;
  const num = typeof raw === "string" ? Number.parseFloat(raw) : raw;
  return Math.round(num);
}

function _atsGetScoreTier(scoreValue) {
  if (scoreValue >= 80) return "excellent";
  if (scoreValue >= 60) return "good";
  return "poor";
}

function _atsSetScoreDisplay(scoreValue) {
  const scoreValueEl = document.getElementById("atsScoreValue");
  if (scoreValueEl) scoreValueEl.textContent = scoreValue;

  const scoreMessage = document.getElementById("atsScoreMessage");
  const tier = _atsGetScoreTier(scoreValue);
  const messages = {
    excellent: { text: "Excellent! Your resume is highly ATS-compatible.", className: "text-success" },
    good: { text: "Good! Some improvements can be made.", className: "text-warning" },
    poor: { text: "Needs improvement for better ATS compatibility.", className: "text-danger" }
  };
  if (scoreMessage) {
    scoreMessage.textContent = messages[tier].text;
    scoreMessage.className = messages[tier].className;
  }

  const scoreCircle = document.querySelector(".ats-score-circle");
  const gradients = {
    excellent: "linear-gradient(135deg, var(--neon-green) 0%, var(--neon-hover) 100%)",
    good: "linear-gradient(135deg, #ffc107 0%, #ff9800 100%)",
    poor: "linear-gradient(135deg, #ff4444 0%, #cc0000 100%)"
  };
  if (scoreCircle) scoreCircle.style.background = gradients[tier];
}

function _atsSetKeywordMatch(percent) {
  const bar = document.getElementById("keywordMatchBar");
  const span = document.getElementById("keywordMatchPercent");
  if (bar) bar.value = percent;
  if (span) span.textContent = percent.toFixed(1) + "%";
}

function _atsSetMissingKeywords(missingKeywords) {
  const div = document.getElementById("missingKeywords");
  if (!div) return;
  div.innerHTML = missingKeywords?.length
    ? missingKeywords.map(kw => "<span class=\"keyword-tag\">" + escapeHtml(kw) + "</span>").join("")
    : '<span class="text-success">No missing keywords detected!</span>';
}

function _atsSetSectionsFound(sections) {
  const div = document.getElementById("sectionsFound");
  if (!div) return;
  const allSections = {
    Summary: sections.summary || false,
    Skills: sections.skills || false,
    Experience: sections.experience || false,
    Education: sections.education || false,
    Projects: sections.projects || false,
    Certifications: sections.certifications || false,
    Languages: sections.languages || false
  };
  div.innerHTML = Object.entries(allSections)
    .map(([name, found]) => {
      const badgeClass = found ? "section-found" : "section-missing";
      const icon = found ? "✓" : "✗";
      return "<span class=\"section-badge " + badgeClass + "\">" + icon + " " + name + "</span>";
    })
    .join("");
}

function _atsSetFormattingIssues(issues, sectionEl, listEl) {
  const hasIssues = issues?.length > 0;
  sectionEl.style.display = hasIssues ? "block" : "none";
  listEl.innerHTML = hasIssues ? issues.map(issue => "<li>" + escapeHtml(issue) + "</li>").join("") : "";
}

function _atsSetAiSuggestions(suggestions, listEl) {
  listEl.innerHTML = suggestions?.length
    ? suggestions.map(s => "<li>" + escapeHtml(s) + "</li>").join("")
    : "<li>No specific suggestions available.</li>";
}

function displayATSResults(data) {
  const scoreValue = _atsNormalizeScore(data);
  _atsSetScoreDisplay(scoreValue);
  _atsSetKeywordMatch(data.keyword_match_percent || 0);
  _atsSetMissingKeywords(data.missing_keywords);
  _atsSetSectionsFound(data.sections_found || {});

  const formattingIssuesSection = document.getElementById("formattingIssuesSection");
  const formattingIssuesList = document.getElementById("formattingIssues");
  if (formattingIssuesSection && formattingIssuesList) {
    _atsSetFormattingIssues(data.formatting_issues, formattingIssuesSection, formattingIssuesList);
  }

  const aiSuggestionsList = document.getElementById("aiSuggestions");
  if (aiSuggestionsList) _atsSetAiSuggestions(data.ai_suggestions, aiSuggestionsList);
}

// Auto open ATS modal if redirected from dashboard
document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(globalThis.location.search);

  if (params.get("openATS") === "true") {
    const modal = document.getElementById("atsCheckModal");
    if (modal) {
      bootstrap.Modal.getOrCreateInstance(modal).show();
    }
  }
});

// Expose handlers for inline onclick (module scope is not global)
globalThis.openResumePreview = openResumePreview;
globalThis.deleteResume = deleteResume;
globalThis.downloadResumeDirect = downloadResumeDirect;
globalThis.downloadResumePDF = downloadResumePDF;
globalThis.addExperienceField = addExperienceField;
globalThis.submitAIResume = submitAIResume;
