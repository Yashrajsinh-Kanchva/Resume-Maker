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

/* ================== LOAD RESUMES ================== */
fetch("/api/resumes", { credentials: "include" })
  .then(res => res.json())
  .then(resumes => {
    const container = document.getElementById("resumeList");

    if (!resumes.length) {
      container.innerHTML = "<p>No resume created</p>";
      return;
    }

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
          ${r.rank === 1 ? "🏆" : r.rank === 2 ? "🥈" : r.rank === 3 ? "🥉" : "🔹"}
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
  });

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
      
      if (!resume || !resume.data) {
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
      
      // Use requestAnimationFrame to ensure DOM is fully rendered
      requestAnimationFrame(() => {
        setTimeout(() => {
          console.log("=== INJECTING DATA ===");
          console.log("Full resume object:", resume);
          console.log("Resume.data:", resume.data);
          console.log("Resume.data.step1:", resume.data?.step1);
          console.log("Resume.data.step2:", resume.data?.step2);
          console.log("Resume.data.step3:", resume.data?.step3);
          console.log("Resume.data.step4:", resume.data?.step4);
          console.log("Resume.data.customSections:", resume.data?.customSections);
          
          if (resume && resume.data) {
            // Verify elements exist before injecting
            console.log("Verifying template elements exist:");
            console.log("previewName exists:", !!document.getElementById("previewName"));
            console.log("previewTitle exists:", !!document.getElementById("previewTitle"));
            console.log("previewEmail exists:", !!document.getElementById("previewEmail"));
            console.log("previewPhone exists:", !!document.getElementById("previewPhone"));
            console.log("previewLocation exists:", !!document.getElementById("previewLocation"));
            console.log("previewSkills exists:", !!document.getElementById("previewSkills"));
            
            injectFinalData(resume.data);
            
            // Verify after injection
            setTimeout(() => {
              console.log("=== AFTER INJECTION ===");
              console.log("previewName content:", document.getElementById("previewName")?.textContent);
              console.log("previewTitle content:", document.getElementById("previewTitle")?.textContent);
              console.log("previewEmail content:", document.getElementById("previewEmail")?.textContent);
              console.log("previewPhone content:", document.getElementById("previewPhone")?.textContent);
              console.log("previewSkills innerHTML:", document.getElementById("previewSkills")?.innerHTML);
            }, 100);
          } else {
            console.error("No resume data found in response");
            alert("Error: Resume data is missing. Please try creating the resume again.");
          }
        }, 100); // Increased timeout to ensure DOM is ready
      });
    })
    .catch(err => {
      console.error("Error loading template:", err);
      alert("Error loading template: " + err.message);
    });
}
/* ================= HELPERS ================= */
function setText(id, value) {
  const el = document.getElementById(id);
  if (el) {
    // Set text even if value is empty string, null, or undefined (to clear fields)
    const textValue = value != null ? String(value) : "";
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
      if (!resume || !resume.data) {
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
          .then(html => {
            tempContainer.innerHTML = html;
            
            // Wait for DOM to be ready and CSS to apply
            requestAnimationFrame(() => {
              setTimeout(() => {
                // Store reference to original finalResumePreview if it exists
                const originalFinalPreview = document.getElementById("finalResumePreview");
                let wasSwapped = false;
                
                // Temporarily swap the container so injectFinalData works
                if (originalFinalPreview && originalFinalPreview.id === "finalResumePreview") {
                  originalFinalPreview.id = "originalFinalResumePreviewBackup";
                  wasSwapped = true;
                }
                
                // Create a wrapper that injectFinalData expects
                const finalPreviewWrapper = document.createElement("div");
                finalPreviewWrapper.id = "finalResumePreview";
                
                // Move the resume content into the wrapper
                const resumeContent = tempContainer.querySelector(".resume");
                if (resumeContent) {
                  finalPreviewWrapper.appendChild(resumeContent);
                } else {
                  // If no .resume class, move all direct children
                  Array.from(tempContainer.children).forEach(child => {
                    finalPreviewWrapper.appendChild(child);
                  });
                }
                
                tempContainer.appendChild(finalPreviewWrapper);
                
                // Inject data into the temporary container
                injectFinalData(resume.data);
                
                // Wait for rendering, fonts, and images to load
                setTimeout(() => {
                  // Find the actual resume element to convert
                  const resumeElement = tempContainer.querySelector(".resume") || 
                                       finalPreviewWrapper.querySelector(".resume") ||
                                       finalPreviewWrapper.firstElementChild ||
                                       tempContainer.firstElementChild;
                  
                  if (!resumeElement || !resumeElement.innerHTML || resumeElement.innerHTML.trim().length === 0) {
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
                  
                  // Ensure resume element has proper width and is not cut off
                  const resumeWidth = 800;
                  resumeElement.style.width = resumeWidth + "px";
                  resumeElement.style.maxWidth = resumeWidth + "px";
                  resumeElement.style.boxSizing = "border-box";
                  
                  // Add CSS to prevent page breaks inside sections
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
                  
                  // Force layout recalculation
                  void resumeElement.offsetHeight;
                  
                  // Get actual content height
                  const actualHeight = Math.max(resumeElement.scrollHeight, resumeElement.offsetHeight);
                  
                  // A4 dimensions: 210mm x 297mm
                  // At 96 DPI: 794px x 1123px
                  // We want to fit content on one page, so calculate scale
                  const a4HeightPx = 1123; // A4 height in pixels
                  const a4WidthPx = 794; // A4 width in pixels
                  
                  // Calculate scale to fit height
                  const heightScale = actualHeight > a4HeightPx ? a4HeightPx / actualHeight : 1;
                  // Calculate scale to fit width (resumeWidth should fit in a4WidthPx)
                  const widthScale = resumeWidth > a4WidthPx ? a4WidthPx / resumeWidth : 1;
                  
                  // Use the smaller scale to ensure everything fits
                  const finalScale = Math.min(heightScale, widthScale, 1);
                  
                  console.log("Resume element dimensions:", {
                    width: resumeElement.offsetWidth,
                    height: actualHeight,
                    scrollHeight: resumeElement.scrollHeight,
                    a4Height: a4HeightPx,
                    heightScale: heightScale,
                    widthScale: widthScale,
                    finalScale: finalScale
                  });
                  
                  // Generate PDF with proper settings to fit on one page
                  html2pdf()
                    .set({
                      margin: [0, 0, 0, 0],
                      filename: `${(resume.title || 'resume').replace(/[^a-z0-9]/gi, '_')}.pdf`,
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
                      pagebreak: { 
                        mode: ['avoid-all', 'css', 'legacy']
                      }
                    })
                    .from(resumeElement)
                    .save()
                    .then(() => {
                      // Remove the style after PDF generation
                      const pdfStyle = document.getElementById("pdf-page-break-style");
                      if (pdfStyle) {
                        document.head.removeChild(pdfStyle);
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
                }, 1000); // Increased wait time for rendering
              }, 200);
            });
          })
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
          if (temp && temp.parentNode) {
            document.body.removeChild(temp);
          }
          
          // Remove temporary CSS if we added it
          if (!existingCSS && cssLink && cssLink.parentNode) {
            document.head.removeChild(cssLink);
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

fetch("/api/resumes/skills/frequency")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("topSkills");
    if (!container) return;

    container.innerHTML = "";

    const entries = Object.entries(data)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6); // show top 6 skills

    if (entries.length === 0) {
      container.innerHTML = "<p class='text-muted'>No skills data available</p>";
      return;
    }

    const maxCount = entries[0][1];

    entries.forEach(([skill, count]) => {
      const percent = Math.round((count / maxCount) * 100);

      container.innerHTML += `
        <div class="skill-row">
          <span class="skill-name">${skill}</span>

          <div class="skill-bar">
            <div class="skill-bar-fill" style="width:${percent}%"></div>
          </div>

          <span class="skill-count">${count}</span>
        </div>
      `;
    });
  });

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
  const role = (roleInput && roleInput.value.trim()) || "";
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

function injectFinalData(data) {
  if (!data) {
    console.warn("No resume data found, trying localStorage fallback");
    // Fallback to localStorage if API data is missing
    data = {
      step1: JSON.parse(localStorage.getItem("step1") || "{}"),
      step2: JSON.parse(localStorage.getItem("step2") || "{}"),
      step3: JSON.parse(localStorage.getItem("experiences") || "[]"),
      step4: JSON.parse(localStorage.getItem("skills") || "[]"),
      customSections: JSON.parse(localStorage.getItem("customSections") || "[]")
    };
    console.log("Using localStorage fallback data:", data);
  }
  
  if (!data.step1) {
    console.warn("No step1 data found in resume data:", data);
  }

  // Scope lookups to the preview container so we always target the loaded template
  const container = document.getElementById("finalResumePreview");
  function getEl(id) {
    return container ? container.querySelector("#" + id) : document.getElementById(id);
  }
  function setTextLocal(id, value) {
    const el = getEl(id);
    if (el) {
      el.textContent = value != null ? String(value) : "";
      if ((value != null ? String(value) : "").trim()) el.style.display = "";
    }
  }

  console.log("=== INJECTING FINAL DATA ===");
  console.log("step1:", JSON.stringify(data.step1, null, 2));
  console.log("step2:", JSON.stringify(data.step2, null, 2));
  console.log("step3:", JSON.stringify(data.step3, null, 2));
  console.log("step4:", JSON.stringify(data.step4, null, 2));

  /* ========== BASIC INFO ========== */
  if (data.step1) {
    const name = (data.step1.name || "").trim();
    const title = (data.step1.title || "").trim();
    const email = (data.step1.email || "").trim();
    const phone = (data.step1.phone || "").trim();
    const location = (data.step1.location || "").trim();
    
    const nameEl = getEl("previewName");
    const titleEl = getEl("previewTitle");
    const emailEl = getEl("previewEmail");
    const phoneEl = getEl("previewPhone");
    const locationEl = getEl("previewLocation");
    
    if (nameEl) {
      nameEl.textContent = name;
      nameEl.style.display = name ? "" : "none";
    }
    if (titleEl) {
      titleEl.textContent = title;
      titleEl.style.display = title ? "" : "none";
    }
    if (emailEl) {
      emailEl.textContent = email;
      emailEl.style.display = email ? "" : "none";
    }
    if (phoneEl) {
      phoneEl.textContent = phone;
      phoneEl.style.display = phone ? "" : "none";
    }
    if (locationEl) {
      locationEl.textContent = location;
      locationEl.style.display = location ? "" : "none";
    }
  }

  /* ========== SKILLS ========== */
  let skills = [];
  if (Array.isArray(data.step4)) {
    skills = data.step4.map(s => typeof s === "string" ? s : s?.name).filter(Boolean);
  } else if (typeof data.step4 === "string" && data.step4.trim()) {
    skills = data.step4.split("\n").map(s => s.trim()).filter(Boolean);
  }

  const skillsBox = getEl("previewSkills");
  const skillsSection = getEl("skillsSection");
  if (skillsBox) {
    console.log("Setting skills:", skills);
    if (skills.length) {
      skillsBox.innerHTML = skills.map(s => `<li>${s}</li>`).join("");
      skillsBox.style.display = "";
      console.log("Skills box innerHTML set to:", skillsBox.innerHTML);
      revealSection(skillsBox);
      if (skillsSection) {
        skillsSection.classList.remove("hide-section");
        skillsSection.style.display = "";
      }
    } else {
      skillsBox.innerHTML = "";
      skillsBox.style.display = "none";
      if (skillsSection) {
        skillsSection.classList.add("hide-section");
        skillsSection.style.display = "none";
      }
    }
  } else {
    console.error("previewSkills element not found!");
  }

  /* ========== SUMMARY ========== */
  const summaryEl = getEl("previewSummary");
  if (summaryEl) {
    const summary = (data.step1?.summary || "").trim();
    if (summary) {
      summaryEl.innerHTML = highlightKeywords(summary, skills);
      summaryEl.style.display = "";
      revealSection(summaryEl);
    } else {
      summaryEl.innerHTML = "";
      summaryEl.style.display = "none";
    }
  }

  /* ========== LANGUAGES ========== */
  const langList = getEl("pLanguages");
  if (langList) {
    // Handle both string (newline-separated) and array formats
    let languages = [];
    if (data.step1) {
      if (Array.isArray(data.step1.languages)) {
        languages = data.step1.languages;
      } else if (typeof data.step1.languages === "string" && data.step1.languages.trim()) {
        languages = data.step1.languages.split("\n").map(l => l.trim()).filter(Boolean);
      }
    }
    
    if (languages.length) {
      langList.innerHTML = languages.map(l => `<li>${l}</li>`).join("");
      langList.style.display = "";
      revealSection(langList);
    } else {
      langList.innerHTML = "";
      langList.style.display = "none";
    }
  }

  /* ========== CERTIFICATIONS ========== */
  const certList = getEl("pCerts");
  if (certList) {
    // Handle both string (newline-separated) and array formats
    // Check for both 'certificates' and 'certs' keys
    let certificates = [];
    if (data.step1) {
      const certData = data.step1.certificates || data.step1.certs;
      
      if (Array.isArray(certData)) {
        certificates = certData;
      } else if (typeof certData === "string" && certData.trim()) {
        certificates = certData.split("\n").map(c => c.trim()).filter(Boolean);
      }
    }
    
    if (certificates.length) {
      certList.innerHTML = certificates.map(c => `<li>${c}</li>`).join("");
      certList.style.display = "";
      revealSection(certList);
    } else {
      certList.innerHTML = "";
      certList.style.display = "none";
    }
  }

  /* ========== EDUCATION ========== */
  if (data.step2) {
    const degree = (data.step2.degree || "").trim();
    const field = (data.step2.field || "").trim();
    const school = (data.step2.school || data.step2.institution || "").trim();
    const location = (data.step2.location || "").trim();
    
    setTextLocal("previewDegree", degree);
    setTextLocal("previewField", field);
    setTextLocal("previewEduInstitute", school);
    setTextLocal("previewEduLocation", location);
    
    if (data.step2.month) {
      const dateText = data.step2.current
        ? `Expected ${formatMonth(data.step2.month)}`
        : formatMonth(data.step2.month);
      setTextLocal("previewGraduation", dateText);
    } else if (data.step2.year) {
      setTextLocal("previewGraduation", (data.step2.year || "").toString().trim());
    } else {
      setTextLocal("previewGraduation", "");
    }

    const eduDetailsEl = getEl("previewEduDetails");
    if (eduDetailsEl && Array.isArray(data.step2.details) && data.step2.details.length) {
      eduDetailsEl.innerHTML = data.step2.details.map(d => `<li>${d}</li>`).join("");
      eduDetailsEl.style.display = "";
    }

    const edu = getEl("educationSection");
    if (edu) {
      if (degree || field || school) {
        edu.classList.remove("hide-section");
        edu.classList.add("show");
        edu.style.display = "";
        if (degree) getEl("previewDegree")?.style.setProperty("display", "", "important");
        if (field) getEl("previewField")?.style.setProperty("display", "", "important");
        if (school) getEl("previewEduInstitute")?.style.setProperty("display", "", "important");
        if (location) getEl("previewEduLocation")?.style.setProperty("display", "", "important");
      } else {
        edu.classList.add("hide-section");
        edu.style.display = "none";
      }
    }
  }

  /* ========== EXPERIENCE ========== */
  if (Array.isArray(data.step3) && data.step3.length) {
    const sec = getEl("previewExperienceSection");
    const list = getEl("previewExperienceList");

    if (sec && list) {
      list.innerHTML = data.step3.map(exp => {
        const jobTitle = exp.jobTitle || "";
        const employer = exp.employer || "";
        const city = exp.city || "";
        const country = exp.country || "";
        const startDate = exp.startMonth || exp.startDate || "";
        const endDate = exp.endMonth || exp.endDate || "";
        const description = exp.description || "";
        
        // Format description as list if it contains newlines
        const descHtml = description.includes("\n")
          ? `<ul>${description.split("\n").filter(Boolean).map(d => `<li>${d}</li>`).join("")}</ul>`
          : `<p>${description}</p>`;
        
        return `
          <div class="mb-3">
            <strong>${jobTitle}${employer ? " – " + employer : ""}</strong><br>
            ${city || country ? `<small>${city}${city && country ? ", " : ""}${country}</small><br>` : ""}
            ${startDate || endDate ? `<small>${startDate}${endDate ? " – " + endDate : ""}</small>` : ""}
            ${descHtml}
          </div>
        `;
      }).join("");

      sec.classList.remove("hide-section");
      sec.classList.add("show");
      sec.style.display = "";
      console.log("Experience section shown with", data.step3.length, "items");
    }
  } else {
    const sec = getEl("previewExperienceSection");
    if (sec) {
      sec.classList.add("hide-section");
      sec.style.display = "none";
    }
  }

  /* ========== CUSTOM SECTIONS ========== */
  const customSections = data.customSections || [];
  
  const root = container || document;
  root.querySelectorAll(".custom-section-final").forEach(el => el.remove());
  
  if (customSections.length) {
    let rightPanel = container ? container.querySelector(".content-column") : document.querySelector(".content-column");
    if (!rightPanel) {
      rightPanel = container ? container.querySelector(".right-panel") : document.querySelector(".right-panel");
    }
    if (!rightPanel) {
      rightPanel = container ? container.querySelector("main") : document.querySelector("main");
    }
    if (!rightPanel) {
      // Fallback: find main content area by looking for sections
      rightPanel =
        (container ? container.querySelector("#previewExperienceSection") : document.querySelector("#previewExperienceSection"))?.parentElement ||
        (container ? container.querySelector("#educationSection") : document.querySelector("#educationSection"))?.parentElement;
    }
    
    console.log("Right panel found:", rightPanel, "Class:", rightPanel?.className, "Tag:", rightPanel?.tagName);
    
    if (rightPanel) {
      // Detect template type by checking existing section classes and structure
      const existingSection = rightPanel.querySelector(".content-card") || rightPanel.querySelector(".main-section") || rightPanel.querySelector(".card-content") || rightPanel.querySelector("section");
      console.log("Existing section found:", existingSection, "Classes:", existingSection?.className);
      
      let sectionClass = "main-section";
      let useWrapper = false;
      let wrapperClass = "";
      
      if (existingSection) {
        // Check for blue-corporate template (uses content-card)
        if (existingSection.classList.contains("content-card")) {
          sectionClass = "content-card";
          console.log("Detected blue-corporate template, using content-card class");
        } 
        // Check for academic-yellow template (uses main-section card-content with inner structure)
        else if (existingSection.classList.contains("card-content")) {
          sectionClass = "main-section card-content";
          useWrapper = true;
          wrapperClass = "content-box";
          console.log("Detected academic-yellow template");
        } 
        // Default to main-section
        else {
          sectionClass = "main-section";
          console.log("Using default main-section class");
        }
      }
      
      customSections.forEach((section, index) => {
        const sectionEl = document.createElement("section");
        sectionEl.className = `${sectionClass} custom-section-final`;
        sectionEl.id = `customSectionFinal${index}`;
        
        // Format description - handle newlines
        const descHtml = section.description.includes("\n")
          ? `<ul>${section.description.split("\n").filter(Boolean).map(d => `<li>${escapeHtml(d)}</li>`).join("")}</ul>`
          : `<p>${escapeHtml(section.description)}</p>`;
        
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
        console.log("Experience section found:", experienceSection, "Display:", experienceSection?.style.display, "Classes:", experienceSection?.className);
        
        if (experienceSection) {
          // Insert after the experience section
          experienceSection.insertAdjacentElement("afterend", sectionEl);
          console.log("✅ Inserted custom section after experience section");
        } else {
          // If no experience section, find the last section or append to the end
          const allSections = rightPanel.querySelectorAll("section");
          const lastSection = allSections[allSections.length - 1];
          console.log("All sections found:", allSections.length, "Last section:", lastSection);
          
          if (lastSection) {
            lastSection.insertAdjacentElement("afterend", sectionEl);
            console.log("✅ Inserted custom section after last section");
          } else {
            rightPanel.appendChild(sectionEl);
            console.log("✅ Appended custom section to end of right panel");
          }
        }
        
        // Ensure section is visible - remove hide-section class and set display
        sectionEl.classList.remove("hide-section");
        sectionEl.style.display = "";
        sectionEl.style.visibility = "visible";
        
        // Force visibility for blue-corporate template (content-card)
        if (sectionClass === "content-card") {
          sectionEl.style.display = "block";
        }
        
        // Verify it's actually in the DOM
        const isInDOM = document.body.contains(sectionEl);
        const computedDisplay = window.getComputedStyle(sectionEl).display;
        const computedVisibility = window.getComputedStyle(sectionEl).visibility;
        
        console.log("✅ Added custom section:", section.name);
        console.log("   Class:", sectionClass);
        console.log("   Element:", sectionEl);
        console.log("   Parent:", sectionEl.parentElement);
        console.log("   In DOM:", isInDOM);
        console.log("   Computed display:", computedDisplay);
        console.log("   Computed visibility:", computedVisibility);
        
        if (!isInDOM || computedDisplay === "none") {
          console.error("❌ Custom section not visible! Display:", computedDisplay, "Visibility:", computedVisibility);
        }
      });
    } else {
      console.error("❌ Right panel not found! Cannot add custom sections.");
    }
  }
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
    k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
  );

  const regex = new RegExp(`\\b(${escaped.join("|")})\\b`, "gi");

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
            } catch (e) {
              // Ignore date parsing errors
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
  
  const form = e.target;
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

function displayATSResults(data) {
  // Display score - use resume_score (same as card/preview) instead of ats_score for consistency
  console.log("displayATSResults called with data:", data);
  console.log("Raw resume_score value:", data.resume_score, "Type:", typeof data.resume_score);
  console.log("Raw ats_score value:", data.ats_score, "Type:", typeof data.ats_score);
  
  // Use resume_score if available (matches card/preview), otherwise fall back to ats_score
  let scoreValue = 0;
  if (data.resume_score !== undefined && data.resume_score !== null) {
    scoreValue = typeof data.resume_score === 'string' ? parseFloat(data.resume_score) : data.resume_score;
    scoreValue = Math.round(scoreValue);
  } else if (data.ats_score !== undefined && data.ats_score !== null) {
    scoreValue = typeof data.ats_score === 'string' ? parseFloat(data.ats_score) : data.ats_score;
    scoreValue = Math.round(scoreValue);
  }
  
  console.log("Calculated scoreValue (using resume_score):", scoreValue);
  
  const scoreValueEl = document.getElementById("atsScoreValue");
  if (scoreValueEl) {
    scoreValueEl.textContent = scoreValue;
    console.log("Set atsScoreValue element to:", scoreValue);
  } else {
    console.error("atsScoreValue element not found!");
  }
  
  // Score message
  const scoreMessage = document.getElementById("atsScoreMessage");
  if (scoreMessage) {
    if (scoreValue >= 80) {
      scoreMessage.textContent = "Excellent! Your resume is highly ATS-compatible.";
      scoreMessage.className = "text-success";
    } else if (scoreValue >= 60) {
      scoreMessage.textContent = "Good! Some improvements can be made.";
      scoreMessage.className = "text-warning";
    } else {
      scoreMessage.textContent = "Needs improvement for better ATS compatibility.";
      scoreMessage.className = "text-danger";
    }
  }
  
  // Update score circle color based on score
  const scoreCircle = document.querySelector(".ats-score-circle");
  if (scoreCircle) {
    if (scoreValue >= 80) {
      scoreCircle.style.background = "linear-gradient(135deg, var(--neon-green) 0%, var(--neon-hover) 100%)";
    } else if (scoreValue >= 60) {
      scoreCircle.style.background = "linear-gradient(135deg, #ffc107 0%, #ff9800 100%)";
    } else {
      scoreCircle.style.background = "linear-gradient(135deg, #ff4444 0%, #cc0000 100%)";
    }
  }
  
  // Keyword match percentage
  const keywordMatchPercent = data.keyword_match_percent || 0;
  const keywordMatchBar = document.getElementById("keywordMatchBar");
  const keywordMatchPercentSpan = document.getElementById("keywordMatchPercent");
  if (keywordMatchBar) {
    keywordMatchBar.style.width = keywordMatchPercent + "%";
  }
  if (keywordMatchPercentSpan) {
    keywordMatchPercentSpan.textContent = keywordMatchPercent.toFixed(1) + "%";
  }
  
  // Missing keywords
  const missingKeywordsDiv = document.getElementById("missingKeywords");
  if (missingKeywordsDiv) {
    if (data.missing_keywords && data.missing_keywords.length > 0) {
      missingKeywordsDiv.innerHTML = data.missing_keywords
        .map(kw => `<span class="keyword-tag">${escapeHtml(kw)}</span>`)
        .join("");
    } else {
      missingKeywordsDiv.innerHTML = '<span class="text-success">No missing keywords detected!</span>';
    }
  }
  
  // Sections found
  const sectionsFoundDiv = document.getElementById("sectionsFound");
  const sections = data.sections_found || {};
  const allSections = {
    "Summary": sections.summary || false,
    "Skills": sections.skills || false,
    "Experience": sections.experience || false,
    "Education": sections.education || false,
    "Projects": sections.projects || false,
    "Certifications": sections.certifications || false,
    "Languages": sections.languages || false
  };
  
  sectionsFoundDiv.innerHTML = Object.entries(allSections)
    .map(([name, found]) => {
      const badgeClass = found ? "section-found" : "section-missing";
      const icon = found ? "✓" : "✗";
      return `<span class="section-badge ${badgeClass}">${icon} ${name}</span>`;
    })
    .join("");
  
  // Formatting issues
  const formattingIssuesSection = document.getElementById("formattingIssuesSection");
  const formattingIssuesList = document.getElementById("formattingIssues");
  if (data.formatting_issues && data.formatting_issues.length > 0) {
    formattingIssuesSection.style.display = "block";
    formattingIssuesList.innerHTML = data.formatting_issues
      .map(issue => `<li>${escapeHtml(issue)}</li>`)
      .join("");
  } else {
    formattingIssuesSection.style.display = "none";
  }
  
  // AI suggestions
  const aiSuggestionsList = document.getElementById("aiSuggestions");
  if (data.ai_suggestions && data.ai_suggestions.length > 0) {
    aiSuggestionsList.innerHTML = data.ai_suggestions
      .map(suggestion => `<li>${escapeHtml(suggestion)}</li>`)
      .join("");
  } else {
    aiSuggestionsList.innerHTML = '<li>No specific suggestions available.</li>';
  }
}

// Auto open ATS modal if redirected from dashboard
document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);

  if (params.get("openATS") === "true") {
    const modal = document.getElementById("atsCheckModal");
    if (modal) {
      bootstrap.Modal.getOrCreateInstance(modal).show();
    }
  }
});
