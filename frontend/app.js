const $ = (id) => document.getElementById(id);

const DEMO_AGENT_ID = "00000000-0000-0000-0000-000000000001";

const state = {
  agentId: DEMO_AGENT_ID,
  apiBase:
    localStorage.getItem("abtalks_api_base") ||
    "https://abtalks-agent-y2jf.onrender.com",
};
$("apiBase").value = state.apiBase;

function apiBase() {
  return $("apiBase").value.trim().replace(/\/+$/, "");
}

function setMessage(text) {
  $("message").textContent = text;
}

function setConnection(online) {
  const badge = $("connectionBadge");
  badge.className = online ? "badge online" : "badge offline";
  badge.textContent = online ? "● Backend online" : "● Backend offline";
}

function setAgent(id) {
  state.agentId = id;
  localStorage.setItem("abtalks_agent_id", id);
  $("agentIdText").textContent = id;
  $("statusText").textContent = "Active";
}

function formatDate(value) {
  if (!value) return "Unknown date";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString();
}

function safeText(value) {
  return String(value ?? "");
}

function renderPosts(posts) {
  const feed = $("feed");
  feed.innerHTML = "";

  $("postCount").textContent = posts.length;

  if (!posts.length) {
    $("emptyState").classList.remove("hidden");
    return;
  }

  $("emptyState").classList.add("hidden");

  for (const post of posts) {
    const article = document.createElement("article");
    article.className = "post";

    const sources = Array.isArray(post.sources) ? post.sources : [];
    const source = sources[0] || "";

    article.innerHTML = `
      <div class="post-header">
        <div class="post-title">${escapeHtml(
          safeText(post.text).split(".")[0] || "AI Security Post"
        )}</div>
        <div class="post-date">${escapeHtml(formatDate(post.createdAt))}</div>
      </div>

      <div class="post-text">${escapeHtml(post.text)}</div>

      <div class="rationale">
        <strong>Why this topic was selected:</strong><br />
        ${escapeHtml(post.rationale || "No rationale provided.")}
      </div>

      <div class="post-footer">
        ${
          source
            ? `<a class="source" href="${escapeAttribute(source)}" target="_blank" rel="noopener noreferrer">
                 View original source ↗
               </a>`
            : "<span class='source'>No source URL</span>"
        }
        <code>${escapeHtml(post.id || "")}</code>
      </div>
    `;

    feed.appendChild(article);
  }
}

function escapeHtml(value) {
  return safeText(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value);
}

async function checkBackend() {
  try {
    const response = await fetch(`${apiBase()}/docs`, {
      method: "GET",
    });
    setConnection(response.ok);
    return response.ok;
  } catch {
    setConnection(false);
    return false;
  }
}

async function initializeAgent() {
  const base = apiBase();
  const name = $("personaName").value.trim();
  const domain = $("personaDomain").value.trim();

  if (!name || !domain) {
    setMessage("Please enter a persona name and domain.");
    return;
  }

  $("initBtn").disabled = true;
  setMessage("Initializing agent...");

  try {
    const response = await fetch(`${base}/api/agent/init`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        persona: {
          name,
          domain,
        },
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || JSON.stringify(data));
    }

    setAgent(data.agentId);
    state.apiBase = base;
    localStorage.setItem("abtalks_api_base", base);

    setMessage(
      "Agent initialized. The autonomous backend cycle has started."
    );

    await refreshFeed();
    setConnection(true);
  } catch (error) {
    setConnection(false);
    setMessage(`Initialization failed: ${error.message}`);
  } finally {
    $("initBtn").disabled = false;
  }
}

async function refreshFeed() {
  if (!state.agentId) {
    setMessage("Initialize an agent first.");
    return;
  }

  $("loading").classList.remove("hidden");
  $("emptyState").classList.add("hidden");

  try {
    const response = await fetch(
  `${apiBase()}/api/agent/feed?agentId=${encodeURIComponent(state.agentId)}&_=${Date.now()}`,
  {
    cache: "no-store"
  }
);

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || JSON.stringify(data));
    }

    renderPosts(data.posts || []);
    $("lastRefresh").textContent = new Date().toLocaleTimeString();
    setConnection(true);
    setMessage("Feed loaded successfully.");
  } catch (error) {
    setConnection(false);
    setMessage(`Could not load feed: ${error.message}`);
    $("emptyState").classList.remove("hidden");
  } finally {
    $("loading").classList.add("hidden");
  }
}

$("initBtn").addEventListener("click", initializeAgent);
$("refreshBtn").addEventListener("click", refreshFeed);
$("refreshTopBtn").addEventListener("click", refreshFeed);

$("apiBase").addEventListener("change", () => {
  state.apiBase = apiBase();
  localStorage.setItem("abtalks_api_base", state.apiBase);
  checkBackend();
});

if (state.agentId) {
  $("agentIdText").textContent = state.agentId;
  $("statusText").textContent = "Previously initialized";
}

checkBackend();

if (state.agentId) {
  refreshFeed();
}

// Refresh the feed every 30 seconds so newly generated posts appear.
setInterval(() => {
  if (state.agentId) refreshFeed();
}, 30000);
