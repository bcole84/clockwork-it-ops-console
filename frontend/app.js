/* IT Ops Console — vanilla JS SPA. No build step, no framework. */

const CONFIG = window.OPS_CONSOLE_CONFIG || {};

const ONBOARDING_STEPS = [
  "Mosyle enrollment complete",
  "SSO / identity account created",
  "Email / calendar provisioned",
  "Slack account created and added to team channels",
  "Jira / Confluence / Bitbucket access granted",
  "1Password vault access granted",
  "Laptop shipped or handed off",
  "Day-1 IT check-in completed",
  'Asset record updated to "In Use"',
];

const OFFBOARDING_STEPS = [
  "SSO / identity account disabled",
  "Slack account removed",
  "Atlassian access revoked",
  "1Password vault access revoked",
  "Email suspended / forwarded per manager",
  "Device remote-locked (if not same-day return)",
  "Device returned and inspected",
  "Device wiped via Mosyle and re-enrolled as spare",
  'Asset record updated to "In Stock" or "Retired"',
];

const DOCS = [
  { file: "new-hire-onboarding.md", title: "New Hire Onboarding" },
  { file: "offboarding-checklist.md", title: "Offboarding Checklist" },
  { file: "mdm-laptop-deployment.md", title: "MDM Laptop Deployment" },
  { file: "ticket-triage-sop.md", title: "Ticket Triage SOP" },
  { file: "network-troubleshooting-guide.md", title: "Network Troubleshooting" },
];

function slug(text) {
  return String(text).toLowerCase().replace(/[^a-z0-9]+/g, "-");
}

async function api(path, options = {}) {
  const res = await fetch(`${CONFIG.apiBaseUrl}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Ops-Console-Key": CONFIG.apiKey || "",
      ...(options.headers || {}),
    },
  });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error((data && data.error) || `Request failed (${res.status})`);
  return data;
}

function escapeHtml(str) {
  return String(str ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

/* ---------------- Tabs ---------------- */
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
  });
});

/* ---------------- Connection status ---------------- */
async function checkConnection() {
  const pill = document.getElementById("connection-status");
  try {
    await api("/assets");
    pill.textContent = "API connected";
    pill.className = "status-pill status-ok";
  } catch (err) {
    pill.textContent = "API unreachable";
    pill.className = "status-pill status-error";
    pill.title = err.message;
  }
}

/* ================= ASSETS ================= */
const assetsForm = document.getElementById("assets-form");
const assetsFormWrap = document.getElementById("assets-form-wrap");

document.getElementById("assets-new-btn").addEventListener("click", () => {
  assetsForm.reset();
  assetsForm.elements.id.value = "";
  assetsFormWrap.classList.remove("hidden");
});
document.getElementById("assets-cancel-btn").addEventListener("click", () => {
  assetsFormWrap.classList.add("hidden");
});

assetsForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(assetsForm);
  const id = fd.get("id");
  const payload = {
    assetType: fd.get("assetType"),
    serialNumber: fd.get("serialNumber"),
    assignedTo: fd.get("assignedTo"),
    status: fd.get("status"),
    purchaseDate: fd.get("purchaseDate"),
    notes: fd.get("notes"),
  };
  if (id) {
    await api(`/assets/${id}`, { method: "PUT", body: JSON.stringify(payload) });
  } else {
    await api("/assets", { method: "POST", body: JSON.stringify(payload) });
  }
  assetsFormWrap.classList.add("hidden");
  loadAssets();
});

async function loadAssets() {
  const items = await api("/assets");
  const tbody = document.getElementById("assets-tbody");
  document.getElementById("assets-empty").classList.toggle("hidden", items.length > 0);
  tbody.innerHTML = items.map((a) => `
    <tr>
      <td>${escapeHtml(a.assetType)}</td>
      <td>${escapeHtml(a.serialNumber)}</td>
      <td>${escapeHtml(a.assignedTo) || "—"}</td>
      <td><span class="badge badge-${slug(a.status)}">${escapeHtml(a.status)}</span></td>
      <td>${escapeHtml(a.purchaseDate) || "—"}</td>
      <td>${escapeHtml(a.notes) || "—"}</td>
      <td>
        <button class="btn-icon" data-edit="${a.id}">Edit</button>
        <button class="btn-icon danger" data-delete="${a.id}">Delete</button>
      </td>
    </tr>`).join("");

  tbody.querySelectorAll("[data-edit]").forEach((btn) => btn.addEventListener("click", () => {
    const item = items.find((a) => a.id === btn.dataset.edit);
    for (const [k, v] of Object.entries(item)) if (assetsForm.elements[k]) assetsForm.elements[k].value = v;
    assetsFormWrap.classList.remove("hidden");
  }));
  tbody.querySelectorAll("[data-delete]").forEach((btn) => btn.addEventListener("click", async () => {
    if (!confirm("Delete this asset?")) return;
    await api(`/assets/${btn.dataset.delete}`, { method: "DELETE" });
    loadAssets();
  }));
}

/* ================= TICKETS ================= */
const ticketsForm = document.getElementById("tickets-form");
const ticketsFormWrap = document.getElementById("tickets-form-wrap");

document.getElementById("tickets-new-btn").addEventListener("click", () => {
  ticketsForm.reset();
  ticketsForm.elements.id.value = "";
  ticketsFormWrap.classList.remove("hidden");
});
document.getElementById("tickets-cancel-btn").addEventListener("click", () => {
  ticketsFormWrap.classList.add("hidden");
});

ticketsForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(ticketsForm);
  const id = fd.get("id");
  const payload = {
    subject: fd.get("subject"),
    description: fd.get("description"),
    requester: fd.get("requester"),
    priority: fd.get("priority"),
    category: fd.get("category"),
    status: fd.get("status"),
    notes: fd.get("notes"),
  };
  if (id) {
    await api(`/tickets/${id}`, { method: "PUT", body: JSON.stringify(payload) });
  } else {
    await api("/tickets", { method: "POST", body: JSON.stringify(payload) });
  }
  ticketsFormWrap.classList.add("hidden");
  loadTickets();
});

async function loadTickets() {
  const items = await api("/tickets");
  const tbody = document.getElementById("tickets-tbody");
  document.getElementById("tickets-empty").classList.toggle("hidden", items.length > 0);
  tbody.innerHTML = items.map((t) => `
    <tr>
      <td>${escapeHtml(t.subject)}</td>
      <td>${escapeHtml(t.requester) || "—"}</td>
      <td><span class="badge badge-${slug(t.priority)}">${escapeHtml(t.priority)}</span></td>
      <td>${escapeHtml(t.category)}</td>
      <td><span class="badge badge-${slug(t.status)}">${escapeHtml(t.status)}</span></td>
      <td>
        <button class="btn-icon" data-edit="${t.id}">Edit</button>
        <button class="btn-icon danger" data-delete="${t.id}">Delete</button>
      </td>
    </tr>`).join("");

  tbody.querySelectorAll("[data-edit]").forEach((btn) => btn.addEventListener("click", () => {
    const item = items.find((t) => t.id === btn.dataset.edit);
    for (const [k, v] of Object.entries(item)) if (ticketsForm.elements[k]) ticketsForm.elements[k].value = v;
    ticketsFormWrap.classList.remove("hidden");
  }));
  tbody.querySelectorAll("[data-delete]").forEach((btn) => btn.addEventListener("click", async () => {
    if (!confirm("Delete this ticket?")) return;
    await api(`/tickets/${btn.dataset.delete}`, { method: "DELETE" });
    loadTickets();
  }));
}

/* ================= ONBOARDING / OFFBOARDING ================= */
const onboardingForm = document.getElementById("onboarding-form");
const onboardingFormWrap = document.getElementById("onboarding-form-wrap");
const onboardingStepsWrap = document.getElementById("onboarding-steps-wrap");

function renderStepsEditor(steps) {
  onboardingStepsWrap.innerHTML = `
    <label style="font-size:12px;font-weight:600;color:var(--text-muted);">Checklist</label>
    <ul class="steps-list" style="margin-top:8px;">
      ${steps.map((s, i) => `
        <li>
          <input type="checkbox" data-step-index="${i}" ${s.done ? "checked" : ""} />
          <span>${escapeHtml(s.label)}</span>
        </li>`).join("")}
    </ul>`;
}

function currentSteps() {
  const boxes = onboardingStepsWrap.querySelectorAll("[data-step-index]");
  return Array.from(boxes).map((box) => ({
    label: box.nextElementSibling.textContent,
    done: box.checked,
  }));
}

function openOnboardingForm(type, existing) {
  onboardingForm.reset();
  onboardingForm.elements.id.value = existing ? existing.id : "";
  onboardingForm.elements.type.value = type;
  document.getElementById("onboarding-date-label").firstChild.textContent =
    type === "Offboarding" ? "Last Day" : "Start Date";
  if (existing) {
    onboardingForm.elements.employeeName.value = existing.employeeName;
    onboardingForm.elements.targetDate.value = existing.targetDate || "";
    onboardingForm.elements.notes.value = existing.notes || "";
    renderStepsEditor(existing.steps || []);
  } else {
    const defaults = (type === "Offboarding" ? OFFBOARDING_STEPS : ONBOARDING_STEPS)
      .map((label) => ({ label, done: false }));
    renderStepsEditor(defaults);
  }
  onboardingFormWrap.classList.remove("hidden");
}

document.getElementById("onboarding-new-btn").addEventListener("click", (e) => openOnboardingForm(e.target.dataset.type));
document.getElementById("offboarding-new-btn").addEventListener("click", (e) => openOnboardingForm(e.target.dataset.type));
document.getElementById("onboarding-cancel-btn").addEventListener("click", () => onboardingFormWrap.classList.add("hidden"));

onboardingForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const fd = new FormData(onboardingForm);
  const id = fd.get("id");
  const payload = {
    employeeName: fd.get("employeeName"),
    type: fd.get("type"),
    targetDate: fd.get("targetDate"),
    notes: fd.get("notes"),
    steps: currentSteps(),
  };
  if (id) {
    await api(`/onboarding/${id}`, { method: "PUT", body: JSON.stringify(payload) });
  } else {
    await api("/onboarding", { method: "POST", body: JSON.stringify(payload) });
  }
  onboardingFormWrap.classList.add("hidden");
  loadOnboarding();
});

async function loadOnboarding() {
  const items = await api("/onboarding");
  const list = document.getElementById("onboarding-list");
  document.getElementById("onboarding-empty").classList.toggle("hidden", items.length > 0);
  list.innerHTML = items.map((o) => {
    const steps = o.steps || [];
    const doneCount = steps.filter((s) => s.done).length;
    const pct = steps.length ? Math.round((doneCount / steps.length) * 100) : 0;
    return `
      <div class="checklist-card">
        <div class="checklist-card-header">
          <div>
            <h3>${escapeHtml(o.employeeName)}</h3>
            <div class="meta">${escapeHtml(o.type)} · ${o.targetDate ? escapeHtml(o.targetDate) : "no date set"}</div>
          </div>
          <span class="badge badge-${slug(o.status)}">${escapeHtml(o.status)}</span>
        </div>
        <div class="progress-bar"><div class="progress-bar-fill" style="width:${pct}%"></div></div>
        <ul class="steps-list">
          ${steps.map((s) => `<li class="${s.done ? "done" : ""}">${s.done ? "✅" : "⬜️"} ${escapeHtml(s.label)}</li>`).join("")}
        </ul>
        <div class="checklist-actions">
          <button class="btn-icon" data-edit="${o.id}">Edit / check off steps</button>
          <button class="btn-icon danger" data-delete="${o.id}">Delete</button>
        </div>
      </div>`;
  }).join("");

  list.querySelectorAll("[data-edit]").forEach((btn) => btn.addEventListener("click", () => {
    const item = items.find((o) => o.id === btn.dataset.edit);
    openOnboardingForm(item.type, item);
  }));
  list.querySelectorAll("[data-delete]").forEach((btn) => btn.addEventListener("click", async () => {
    if (!confirm("Delete this checklist?")) return;
    await api(`/onboarding/${btn.dataset.delete}`, { method: "DELETE" });
    loadOnboarding();
  }));
}

/* ================= KNOWLEDGE BASE ================= */
function initDocs() {
  const list = document.getElementById("docs-list");
  list.innerHTML = DOCS.map((d) => `<li><button data-file="${d.file}">${escapeHtml(d.title)}</button></li>`).join("");
  list.querySelectorAll("button").forEach((btn) => btn.addEventListener("click", () => loadDoc(btn)));
}

async function loadDoc(btn) {
  document.querySelectorAll("#docs-list button").forEach((b) => b.classList.remove("active"));
  btn.classList.add("active");
  const content = document.getElementById("docs-content");
  content.innerHTML = "<p class=\"empty-state\">Loading…</p>";
  try {
    const res = await fetch(`docs/${btn.dataset.file}`);
    const md = await res.text();
    content.innerHTML = marked.parse(md);
  } catch (err) {
    content.innerHTML = `<p class="empty-state">Couldn't load this document.</p>`;
  }
}

/* ================= INIT ================= */
checkConnection();
loadAssets();
loadTickets();
loadOnboarding();
initDocs();
