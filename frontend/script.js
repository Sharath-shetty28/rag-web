const BASE_URL = "http://127.0.0.1:8000/api"; // your FastAPI backend

// ---- Crawl ----
document.getElementById("crawlForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const start_url = document.getElementById("start_url").value;
  const max_pages = document.getElementById("max_pages").value || 20;
  const crawl_delay_ms = document.getElementById("crawl_delay_ms").value || 0.5;

  const res = await fetch(`${BASE_URL}/crawl`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start_url, max_pages, crawl_delay_ms }),
  });

  const data = await res.json();
  document.getElementById("crawlResult").textContent = JSON.stringify(
    data,
    null,
    2
  );
});

// ---- Index ----
document.getElementById("indexForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const embedding_model =
    document.getElementById("embedding_model").value || "all-MiniLM-L6-v2";

  const res = await fetch(`${BASE_URL}/index`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ embedding_model }),
  });

  const data = await res.json();
  document.getElementById("indexResult").textContent = JSON.stringify(
    data,
    null,
    2
  );
});

// ---- Ask ----
document.getElementById("askForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = document.getElementById("question").value;
  const top_k = document.getElementById("top_k").value || 3;

  const res = await fetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, top_k }),
  });

  const data = await res.json();
  document.getElementById("askResult").textContent = JSON.stringify(
    data,
    null,
    2
  );
});
