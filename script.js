const uploadEl = document.getElementById("pdf-upload");
const chatEl   = document.getElementById("chat");
const qInput   = document.getElementById("question");
const askBtn   = document.getElementById("ask-btn");

const BACKEND = "http://localhost:8000";  // match your uvicorn port

// 1) Upload PDF
uploadEl.addEventListener("change", async () => {
  const file = uploadEl.files[0];
  if (!file) return;
  const data = new FormData();
  data.append("file", file);
  const res = await fetch(`${BACKEND}/upload`, {
    method: "POST", body: data
  });
  console.log(await res.json());
});

// 2) Ask question
askBtn.addEventListener("click", async () => {
  const question = qInput.value.trim();
  if (!question) return;
  chatEl.innerHTML += `<div class="message you">${question}</div>`;
  const res = await fetch(`${BACKEND}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });
  const { answer } = await res.json();
  chatEl.innerHTML += `<div class="message bot">${answer}</div>`;
  qInput.value = "";
  chatEl.scrollTop = chatEl.scrollHeight;
});
//