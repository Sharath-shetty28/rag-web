const BASE_URL = "http://127.0.0.1:8000"; // your FastAPI backend

// ---- Crawl ----
document.getElementById("crawlForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const start_url = document.getElementById("start_url").value;
  const max_pages = parseInt(document.getElementById("max_pages").value) || 20;
  const max_depth = parseInt(document.getElementById("max_depth").value) || 2;
  const crawl_delay_ms =
    parseFloat(document.getElementById("crawl_delay_ms").value) || 0.5;

  const res = await fetch(`${BASE_URL}/crawl`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start_url, max_pages, max_depth, crawl_delay_ms }),
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

  const chunk_size =
    parseInt(document.getElementById("chunk_size").value) || 500;
  const chunk_overlap =
    parseInt(document.getElementById("chunk_overlap").value) || 50;
  const embedding_model =
    document.getElementById("embedding_model").value || "all-MiniLM-L6-v2";

  const res = await fetch(`${BASE_URL}/index`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chunk_size, chunk_overlap, embedding_model }),
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
  const top_k = parseInt(document.getElementById("top_k").value) || 3;

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
