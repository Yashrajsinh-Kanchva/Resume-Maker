function goBack() {
  fetch("/api/resumes/navigation/back", {
    method: "POST"
  })
    .then(res => res.json())
    .then(data => {
      if (data.current === "preview") {
        globalThis.location.href = "/preview.html";
      } else {
        globalThis.location.href = "/documents.html";
      }
    });
}
