(() => {
  const app = document.getElementById("interest-app");
  if (!app) return;

  const grid = document.getElementById("interest-grid");
  const loadingState = document.getElementById("interest-loading");
  const errorState = document.getElementById("interest-error");
  const emptyState = document.getElementById("interest-empty");
  const searchForm = document.getElementById("interest-search-form");
  const searchInput = document.getElementById("interest-search-input");
  function getCsrfToken() {
    const cookie = document.cookie
      .split(";")
      .map((value) => value.trim())
      .find((value) => value.startsWith("csrftoken="));
    if (cookie) return decodeURIComponent(cookie.slice("csrftoken=".length));
    return (
      document.querySelector("#interest-csrf-form [name=csrfmiddlewaretoken]")
        ?.value || ""
    );
  }
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
    button.type = "button";
    button.className = className;
    button.textContent = text;
    return button;
  }

  function apiErrorMessage(data, status) {
    const messages = Object.values(data)
      .flat()
      .filter((value) => typeof value === "string");
    return messages.join(" ") || `Request failed (HTTP ${status}).`;
  }

  async function writeInterest(url, method, payload) {
    const response = await fetch(url, {
      method,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
      body: payload === undefined ? undefined : JSON.stringify(payload),
    });
    if (response.status === 204) return null;
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(apiErrorMessage(data, response.status));
    return data;
  }

  function makeItemUrl(template, id) {
    return template.replace(
      "00000000-0000-0000-0000-000000000000",
      encodeURIComponent(id),
    );
  }

  function createInterestCard(item) {
    const fields = item;
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
      const starButton = makeButton(
        `${fields.is_starred ? "★ Unstar" : "★ Star"} ${fields.star_count}`,
        `button button-star${fields.is_starred ? " is-starred" : ""}`,
      );
      starButton.title = `${fields.star_count} star`;
      starButton.addEventListener("click", () =>
        runAction(
          starButton,
          makeItemUrl(app.dataset.starUrlTemplate, item.id),
          "POST",
          "Star diperbarui.",
        ),
      );
      actions.append(starButton);
    } else {
      const count = document.createElement("span");
      count.className = "star-count";
      count.textContent = `${fields.star_count} star`;
      actions.append(count);
    }

    if (app.dataset.canEdit === "true") {
      const editLink = document.createElement("a");
      editLink.className = "button button-secondary";
      editLink.href = makeItemUrl(app.dataset.editUrlTemplate, item.id);
      editLink.textContent = "Edit";
      actions.append(editLink);
    }

    if (app.dataset.canDelete === "true") {
      const deleteButton = makeButton("Hapus", "button button-danger");
      deleteButton.addEventListener("click", () => {
        if (!window.confirm("Yakin ingin menghapus interest ini?")) return;
        runAction(
          deleteButton,
          makeItemUrl(app.dataset.deleteUrlTemplate, item.id),
          "DELETE",
          "Interest dihapus.",
        );
      });
      actions.append(deleteButton);
    }

    card.append(header, description, actions);
    return card;
  }

  async function runAction(button, url, method, successMessage) {
    if (button.disabled) return;
    button.disabled = true;
    try {
      await writeInterest(url, method);
      showToast("Berhasil", successMessage, "success");
      await loadInterests(searchInput.value.trim());
    } catch (error) {
      showToast("Permintaan gagal", error.message, "error");
      button.disabled = false;
    }
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
        const fields = new FormData(interestForm);
        const since = String(fields.get("since") ?? "").trim();
        await writeInterest(app.dataset.listUrl, "POST", {
          title: fields.get("title"),
          description: fields.get("description"),
          since: since === "" ? null : Number(since),
        });

        interestForm.reset();
        document.getElementById("add-interest-modal").hidePopover();
        showToast("Berhasil", "Interest berhasil ditambahkan.", "success");
        await loadInterests(searchInput.value.trim());
      } catch (error) {
        console.error("Error adding interest:", error);
        showToast("Gagal menambahkan interest", error.message, "error");
      } finally {
        submitButton.disabled = false;
      }
    });
  }

  loadInterests();
})();
