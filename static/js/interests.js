(() => {
  const app = document.getElementById("interest-app");
  if (!app) return;

  const grid = document.getElementById("interest-grid");
  const loadingState = document.getElementById("interest-loading");
  const errorState = document.getElementById("interest-error");
  const emptyState = document.getElementById("interest-empty");
  const searchForm = document.getElementById("interest-search-form");
  const searchInput = document.getElementById("interest-search-input");
  const csrfToken =
    document.querySelector("#interest-csrf-form [name=csrfmiddlewaretoken]")
      ?.value || "";
  const debounceDelay = 300;
  let debounceTimer;
  let activeRequest;

  function showState(state) {
    loadingState.classList.toggle("hide", state !== "loading");
    errorState.classList.toggle("hide", state !== "error");
    emptyState.classList.toggle("hide", state !== "empty");
    grid.classList.toggle("hide", state !== "results");
  }

  function makeButton(text, className) {
    const button = document.createElement("button");
    button.type = "submit";
    button.className = className;
    button.textContent = text;
    return button;
  }

  function setCsrfToken(form) {
    const tokenInput = document.createElement("input");
    tokenInput.type = "hidden";
    tokenInput.name = "csrfmiddlewaretoken";
    tokenInput.value = csrfToken;
    form.append(tokenInput);
  }

  function makeItemUrl(template, id) {
    return template.replace(
      "00000000-0000-0000-0000-000000000000",
      encodeURIComponent(id),
    );
  }

  function createInterestCard(item) {
    const fields = item.fields;
    const card = document.createElement("article");
    card.className = "interest-card";

    const header = document.createElement("div");
    header.className = "interest-header";
    const title = document.createElement("h2");
    title.textContent = fields.title;
    const year = document.createElement("span");
    year.className = "interest-year";
    year.textContent = fields.since ?? "—";
    header.append(title, year);

    const description = document.createElement("p");
    description.className = "interest-description";
    description.textContent = fields.description;

    const actions = document.createElement("div");
    actions.className = "card-actions";

    if (app.dataset.canStar === "true") {
      const starForm = document.createElement("form");
      starForm.method = "post";
      starForm.action = makeItemUrl(app.dataset.starUrlTemplate, item.pk);
      starForm.className = "star-form";
      setCsrfToken(starForm);

      const starButton = makeButton(
        `${fields.is_starred ? "★ Unstar" : "★ Star"} ${fields.star_count}`,
        `button button-star${fields.is_starred ? " is-starred" : ""}`,
      );
      starButton.title = `${fields.star_count} star`;
      starForm.append(starButton);
      actions.append(starForm);
    } else {
      const count = document.createElement("span");
      count.className = "star-count";
      count.textContent = `${fields.star_count} star`;
      actions.append(count);
    }

    if (app.dataset.canEdit === "true") {
      const editLink = document.createElement("a");
      editLink.className = "button button-secondary";
      editLink.href = makeItemUrl(app.dataset.editUrlTemplate, item.pk);
      editLink.textContent = "Edit";
      actions.append(editLink);
    }

    if (app.dataset.canDelete === "true") {
      const deleteForm = document.createElement("form");
      deleteForm.method = "post";
      deleteForm.action = makeItemUrl(app.dataset.deleteUrlTemplate, item.pk);
      deleteForm.className = "inline-form";
      setCsrfToken(deleteForm);
      const deleteButton = makeButton("Hapus", "button button-danger");
      deleteButton.addEventListener("click", (event) => {
        if (!window.confirm("Yakin ingin menghapus interest ini?")) {
          event.preventDefault();
        }
      });
      deleteForm.append(deleteButton);
      actions.append(deleteForm);
    }

    card.append(header, description, actions);
    return card;
  }

  async function loadInterests(query = "") {
    activeRequest?.abort();
    activeRequest = new AbortController();
    showState("loading");

    const url = new URL(app.dataset.listUrl, window.location.href);
    if (query) url.searchParams.set("title", query);

    try {
      const response = await fetch(url, {
        headers: { Accept: "application/json" },
        signal: activeRequest.signal,
      });
      if (!response.ok) {
        throw new Error(`Gagal memuat interest (status ${response.status}).`);
      }

      const data = await response.json();
      grid.replaceChildren();
      if (data.length === 0) {
        showState("empty");
        return;
      }

      data.forEach((item) => grid.append(createInterestCard(item)));
      showState("results");
    } catch (error) {
      if (error.name === "AbortError") return;
      console.error("Error loading interests:", error);
      showState("error");
    }
  }

  searchInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(
      () => loadInterests(searchInput.value.trim()),
      debounceDelay,
    );
  });

  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    clearTimeout(debounceTimer);
    loadInterests(searchInput.value.trim());
  });

  document
    .getElementById("interest-retry")
    .addEventListener("click", () => loadInterests(searchInput.value.trim()));

  const interestForm = document.getElementById("interest-form");
  if (interestForm) {
    interestForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const submitButton = interestForm.querySelector('[type="submit"]');
      submitButton.disabled = true;

      try {
        const response = await fetch(interestForm.action, {
          method: "POST",
          headers: { Accept: "application/json" },
          body: new FormData(interestForm),
        });
        const result = await response.json();
        if (!response.ok) {
          const messages = result.errors
            ? Object.values(result.errors)
                .flat()
                .map((error) => error.message)
            : [result.message || `Terjadi kesalahan (status ${response.status}).`];
          showToast("Gagal menambahkan interest", messages.join(" "), "error");
          return;
        }

        interestForm.reset();
        document.getElementById("add-interest-modal").hidePopover();
        showToast("Berhasil", result.message, "success");
        await loadInterests(searchInput.value.trim());
      } catch (error) {
        console.error("Error adding interest:", error);
        showToast(
          "Gagal menambahkan interest",
          "Tidak dapat terhubung ke server. Silakan coba lagi.",
          "error",
        );
      } finally {
        submitButton.disabled = false;
      }
    });
  }

  loadInterests();
})();
