const API_BASE = "/api";

function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}

function formatDate(isoString) {
  return new Date(isoString).toLocaleString();
}

function typeBadge(type) {
  const classes = {
    credit: "badge-credit",
    debit: "badge-debit",
    transfer: "badge-transfer",
  };
  const cls = classes[type] || "bg-gray-100 text-gray-600";
  return `<span class="px-2 py-1 rounded-full text-xs font-medium ${cls}">${type}</span>`;
}

function setHealth(ok, message) {
  const dot = document.getElementById("health-dot");
  const text = document.getElementById("health-text");
  dot.className = `health-dot ${ok ? "health-ok" : "health-error"}`;
  text.textContent = message;
}

async function checkHealth() {
  try {
    const res = await fetch("/health");
    if (!res.ok) throw new Error("unhealthy");
    const data = await res.json();
    setHealth(true, `Healthy (${data.hostname})`);
    document.getElementById("info-host").textContent = data.hostname;
  } catch {
    setHealth(false, "Unhealthy");
  }
}

async function loadConfig() {
  try {
    const res = await fetch(`${API_BASE}/config`);
    const data = await res.json();
    document.getElementById("version-badge").textContent = `v${data.version}`;
    document.getElementById("info-version").textContent = data.version;
    document.getElementById("info-theme").textContent = data.theme;
    document.body.className = `theme-${data.theme} bg-gray-50 min-h-screen`;
  } catch {
    document.getElementById("info-theme").textContent = "unknown";
  }
}

async function loadStats() {
  const res = await fetch(`${API_BASE}/stats`);
  const data = await res.json();
  document.getElementById("stat-count").textContent = data.total_transactions;
  document.getElementById("stat-credit").textContent = formatCurrency(data.total_credit);
  document.getElementById("stat-debit").textContent = formatCurrency(data.total_debit);
  document.getElementById("stat-balance").textContent = formatCurrency(data.net_balance);
}

async function loadTransactions() {
  const res = await fetch(`${API_BASE}/transactions?limit=20`);
  const data = await res.json();
  const tbody = document.getElementById("transactions-body");

  if (data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="px-6 py-8 text-center text-gray-400">No transactions yet</td></tr>`;
    return;
  }

  tbody.innerHTML = data
    .map(
      (tx) => `
    <tr class="hover:bg-gray-50">
      <td class="px-6 py-3 font-mono text-gray-600">#${tx.id}</td>
      <td class="px-6 py-3">${typeBadge(tx.type)}</td>
      <td class="px-6 py-3 font-semibold">${formatCurrency(tx.amount)}</td>
      <td class="px-6 py-3">${tx.description}</td>
      <td class="px-6 py-3 font-mono text-xs">${tx.account_from}</td>
      <td class="px-6 py-3 font-mono text-xs">${tx.account_to}</td>
      <td class="px-6 py-3"><span class="text-green-600 text-xs font-medium">${tx.status}</span></td>
      <td class="px-6 py-3 text-gray-500">${formatDate(tx.created_at)}</td>
    </tr>`
    )
    .join("");
}

async function refreshAll() {
  await Promise.all([checkHealth(), loadConfig(), loadStats(), loadTransactions()]);
}

async function generateTransaction() {
  const btn = document.getElementById("generate-btn");
  btn.disabled = true;
  btn.textContent = "Generating...";
  try {
    await fetch(`${API_BASE}/transactions/generate`, { method: "POST" });
    await refreshAll();
  } finally {
    btn.disabled = false;
    btn.textContent = "Generate Transaction";
  }
}

document.getElementById("refresh-btn").addEventListener("click", refreshAll);
document.getElementById("generate-btn").addEventListener("click", generateTransaction);

refreshAll();
setInterval(checkHealth, 15000);
