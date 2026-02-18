/* ===================================================== */
/* ================= TEMPLATE DATA ===================== */
/* ===================================================== */

const templates = [
  {
    key: "academicYellow",
    img: "../IMG/template1.png",
    name: "Professional",
    desc: "A clean professional layout suitable for all roles."
  },
  {
    key: "professionalBlue",
    img: "../IMG/template2.png",
    name: "Modern",
    desc: "A modern design with strong visual hierarchy."
  },
  {
    key: "minimalElegant",
    img: "../IMG/template3.png",
    name: "Creative",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "blueCorporate",
    img:"../IMG/template4.png",
    name: "Blue-Corporate",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "softGreenMinimal",
    img:"../IMG/template5.png",
    name: "Soft-Green-Minimal",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "darkElegant",
    img:"../IMG/template6.png",
    name: "Dark-Elegant",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "timelineResume",
    img:"../IMG/template7.png",
    name: "Timeline-Resume",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "cardBased",
    img:"../IMG/template8.png",
    name: "Card-Based",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "boldRedAccent",
    img:"../IMG/template9.png",
    name: "Bold-Red-Accent",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "glassmorphism",
    img:"../IMG/template1.png",
    name: "Glassmorphism",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "infographic",
    img:"../IMG/template2.png",
    name: "Infographic",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "ultraMinimal",
    img:"../IMG/template3.png",
    name: "Ultra-Minimal",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "boxShadow",
    img:"../IMG/template4.png",
    name: "Box-Shadow",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "classicSerif",
    img:"../IMG/template5.png",
    name: "Classic-Serif",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "freshGradient",
    img:"../IMG/template6.png",
    name: "Fresh-Gradient",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "splitHeaderModern",
    img:"../IMG/template7.png",
    name: "Split-Header-Modern",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "techLook",
    img:"../IMG/template8.png",
    name: "Tech-Look",
    desc: "A creative layout for designers and innovators."
  },
  {
    key: "ultraClean",
    img:"../IMG/template9.png",
    name: "Ultra-Clean",
    desc: "A creative layout for designers and innovators."
  }
];

let i = 0;

/* ===================================================== */
/* ================= DOM ELEMENTS ====================== */
/* ===================================================== */

const mainCard = document.querySelector(".main img");
const back1Card = document.querySelector(".back1 img");
const back2Card = document.querySelector(".back2 img");

const nameBox = document.getElementById("tempName");
const descBox = document.getElementById("tempDesc");

const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");

/* ===================================================== */
/* ================= SAFETY CHECK ====================== */
/* ===================================================== */

const carouselReady =
  mainCard && back1Card && back2Card && nameBox && descBox;

/* ===================================================== */
/* ================= UPDATE CARDS ====================== */
/* ===================================================== */

function updateCards() {
  if (!carouselReady) return;

  mainCard.src = templates[i].img;
  back1Card.src = templates[(i + 1) % templates.length].img;
  back2Card.src = templates[(i + 2) % templates.length].img;

  nameBox.textContent = templates[i].name;
  descBox.textContent = templates[i].desc;
}

/* ===================================================== */
/* ================= ANIMATION ========================= */
/* ===================================================== */

function animateTransition(direction) {
  if (!carouselReady) return;

  const mainDiv = document.querySelector(".main");
  if (!mainDiv) return;

  if (direction === "next") {
    mainDiv.classList.add("slide-out-left");
  } else {
    mainDiv.classList.add("slide-in-right");
  }

  setTimeout(() => {
    updateCards();

    mainDiv.classList.remove("slide-out-left", "slide-in-right");
    mainDiv.classList.add("active");

    setTimeout(() => {
      mainDiv.classList.remove("active");
    }, 400);
  }, 300);
}

/* ===================================================== */
/* ================= NAV BUTTONS ======================= */
/* ===================================================== */

if (nextBtn && prevBtn && carouselReady) {
  nextBtn.onclick = () => {
    i = (i + 1) % templates.length;
    animateTransition("next");
  };

  prevBtn.onclick = () => {
    i = (i - 1 + templates.length) % templates.length;
    animateTransition("prev");
  };
}

/* ===================================================== */
/* ================= AUTO ROTATE ======================= */
/* ===================================================== */

if (carouselReady) {
  setInterval(() => {
    i = (i + 1) % templates.length;
    animateTransition("next");
  }, 6000);
}

/* ===================================================== */
/* ================= INITIAL LOAD ====================== */
/* ===================================================== */

updateCards();

/* ===================================================== */
/* ========== TEMPLATE SELECTION (IMPORTANT) ============ */
/* ===================================================== */

document.querySelectorAll(".use-btn").forEach((btn, index) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();

    const selectedTemplate = templates[index].key;

    console.log("Template selected:", selectedTemplate);

    // Save selected template
    localStorage.setItem("selectedTemplate", selectedTemplate);

    // Optional: clear previous resume data
    localStorage.removeItem("step1");
    localStorage.removeItem("experiences");
    localStorage.removeItem("education");
    localStorage.removeItem("skills");

    // Go to Step-1
    globalThis.location.href = "step-1.html";
  });
});

/* ===================================================== */
/* ================= FILTER LOGIC ====================== */
/* ===================================================== */

const filterButtons = document.querySelectorAll(".filter-btn");
const templateCards = document.querySelectorAll(".template-card");

filterButtons.forEach(btn => {
  btn.addEventListener("click", () => {

    // Active button UI
    filterButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    const filterValue = btn.dataset.filter;

    templateCards.forEach(card => {
      const categories = card.dataset.category;

      if (filterValue === "all") {
        card.classList.remove("hide");
      }
      else if (categories.includes(filterValue)) {
        card.classList.remove("hide");
      }
      else {
        card.classList.add("hide");
      }
    });
  });
});

