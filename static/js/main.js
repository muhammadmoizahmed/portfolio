document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("gallery-modal");
  const imgEl = document.getElementById("gallery-image");
  const titleEl = document.getElementById("gallery-title");
  const linkEl = document.getElementById("gallery-link");
  const btnPrev = document.getElementById("gallery-prev");
  const btnNext = document.getElementById("gallery-next");
  const btnClose = document.getElementById("gallery-close");
  const panel = document.getElementById("gallery-panel");
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
    modal.classList.add("flex", "transition-opacity", "duration-200", "opacity-0");
    if (panel) {
      panel.classList.add("transition-all", "duration-200", "opacity-0", "scale-95");
    }
    requestAnimationFrame(() => {
      modal.classList.remove("opacity-0");
      if (panel) panel.classList.remove("opacity-0", "scale-95");
    });
    document.body.classList.add("overflow-hidden");
  }
  function closeGallery() {
    if (!modal.classList.contains("hidden")) {
      modal.classList.add("opacity-0");
      if (panel) panel.classList.add("opacity-0", "scale-95");
      setTimeout(() => {
        modal.classList.add("hidden");
        modal.classList.remove("flex", "transition-opacity", "duration-200", "opacity-0");
        if (panel) panel.classList.remove("transition-all", "duration-200", "opacity-0", "scale-95");
        images = [];
        index = 0;
        imgEl.src = "";
        titleEl.textContent = "";
        linkEl.innerHTML = "";
      }, 180);
    }
    document.body.classList.remove("overflow-hidden");
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
  document.addEventListener("keydown", (e) => {
    if (modal && !modal.classList.contains("hidden")) {
      if (e.key === "Escape") closeGallery();
      if (e.key === "ArrowRight") nextImage();
      if (e.key === "ArrowLeft") prevImage();
    }
  });

  // Table utilities (search, sort, paginate) - activated when elements present
  function enhanceTables() {
    document.querySelectorAll('[data-table]')?.forEach(container => {
      const table = container.querySelector('table');
      if (!table) return;
      const rows = Array.from(table.tBodies[0]?.rows || []);
      const searchInput = container.querySelector('[data-table-search]');
      const pageSize = parseInt(container.getAttribute('data-table-page-size') || '10', 10);
      let page = 1;
      let filtered = rows.slice();
      let sort = { idx: -1, dir: 1 };

      function render() {
        const start = (page - 1) * pageSize;
        const end = start + pageSize;
        rows.forEach(r => r.style.display = 'none');
        filtered.slice(start, end).forEach(r => r.style.display = '');
        const pager = container.querySelector('[data-table-pager]');
        if (pager) pager.textContent = `${Math.min(end, filtered.length)} / ${filtered.length}`;
      }

      function applySearch() {
        const q = (searchInput?.value || '').toLowerCase();
        filtered = rows.filter(r => r.textContent.toLowerCase().includes(q));
        page = 1; render();
      }

      function applySort(idx) {
        if (sort.idx === idx) sort.dir *= -1; else { sort.idx = idx; sort.dir = 1; }
        filtered.sort((a, b) => {
          const av = a.cells[idx]?.textContent.trim().toLowerCase() || '';
          const bv = b.cells[idx]?.textContent.trim().toLowerCase() || '';
          return av.localeCompare(bv) * sort.dir;
        });
        page = 1; render();
      }

      // Header sorting
      table.tHead && Array.from(table.tHead.rows[0].cells).forEach((th, i) => {
        if (th.hasAttribute('data-sort')) {
          th.style.cursor = 'pointer';
          th.addEventListener('click', () => applySort(i));
        }
      });

      // Search
      if (searchInput) searchInput.addEventListener('input', applySearch);

      // Pagination controls
      const btnPrev = container.querySelector('[data-table-prev]');
      const btnNext = container.querySelector('[data-table-next]');
      btnPrev && btnPrev.addEventListener('click', () => { if (page > 1) { page--; render(); } });
      btnNext && btnNext.addEventListener('click', () => {
        const maxPage = Math.max(1, Math.ceil(filtered.length / pageSize));
        if (page < maxPage) { page++; render(); }
      });

      // Initial
      applySearch();
    });
  }
  enhanceTables();
});
