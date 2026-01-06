document.addEventListener("DOMContentLoaded", function () {
  if (window.AOS && typeof AOS.init === "function") {
    AOS.init({ duration: 600, once: true });
  }
  const modal = document.getElementById("gallery-modal");
  const imgEl = document.getElementById("gallery-image");
  const titleEl = document.getElementById("gallery-title");
  const linkEl = document.getElementById("gallery-link");
  const btnPrev = document.getElementById("gallery-prev");
  const btnNext = document.getElementById("gallery-next");
  const btnClose = document.getElementById("gallery-close");
  let images = [];
  let index = 0;
  function updateImage() {
    if (!images.length) {
      imgEl.src = "";
      return;
    }
    const imgUrl = images[index];
    if (imgUrl.startsWith("http")) {
      imgEl.src = imgUrl;
    } else {
      imgEl.src = "/static/uploads/" + imgUrl;
    }
  }

  function openGallery(title, imgs, link) {
    images = Array.isArray(imgs) ? imgs : [];
    index = 0;
    titleEl.textContent = title || "Project";
    updateImage();
    linkEl.innerHTML = link ? `<a href="${link}" target="_blank" class="text-teal-400 hover:underline">Open Repository</a>` : "";
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  }
  function closeGallery() {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    images = [];
    index = 0;
    imgEl.src = "";
    titleEl.textContent = "";
    linkEl.innerHTML = "";
  }
  function nextImage() {
    if (!images.length) return;
    index = (index + 1) % images.length;
    updateImage();
  }
  function prevImage() {
    if (!images.length) return;
    index = (index - 1 + images.length) % images.length;
    updateImage();
  }
  document.querySelectorAll(".project-card").forEach(card => {
    card.addEventListener("click", () => {
      const imgs = JSON.parse(card.getAttribute("data-images") || "[]");
      const title = card.getAttribute("data-title") || "";
      const link = card.getAttribute("data-link") || "";
      openGallery(title, imgs, link);
    });
  });
  btnClose.addEventListener("click", closeGallery);
  btnNext.addEventListener("click", nextImage);
  btnPrev.addEventListener("click", prevImage);
  modal.addEventListener("click", e => { if (e.target === modal) closeGallery(); });
});
