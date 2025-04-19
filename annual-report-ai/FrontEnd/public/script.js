const uploadEl = document.getElementById("pdf-upload");
const chatEl = document.getElementById("chat");
const qInput = document.getElementById("question");
const askBtn = document.getElementById("ask-btn");

const BACKEND = "http://localhost:8000";
let currentFileId = null;

// 1) Upload PDF
uploadEl.addEventListener("change", async () => {
  const file = uploadEl.files[0];
  if (!file) return;
  
  const data = new FormData();
  data.append("file", file);
  
  try {
    const res = await fetch(`${BACKEND}/upload`, {
      method: "POST",
      body: data
    });
    const result = await res.json();
    currentFileId = result.file_id;
    console.log("File uploaded with ID:", currentFileId);
  } catch (error) {
    console.error("Upload failed:", error);
  }
});

// 2) Ask question
askBtn.addEventListener("click", async () => {
  const question = qInput.value.trim();
  if (!question) return;
  
  // Add user question to chat
  chatEl.innerHTML += `<div class="message you">${question}</div>`;
  
  try {
    const formData = new FormData();
    formData.append("question", question);
    if (currentFileId) {
      formData.append("file_id", currentFileId);
    }
    
    const res = await fetch(`${BACKEND}/ask`, {
      method: "POST",
      body: formData
    });
    
    const { answer, error } = await res.json();
    if (error) {
      chatEl.innerHTML += `<div class="message error">${error}</div>`;
    } else {
      chatEl.innerHTML += `<div class="message bot">${answer}</div>`;
    }
  } catch (error) {
    chatEl.innerHTML += `<div class="message error">Failed to get answer</div>`;
    console.error("Error:", error);
  }
  
  qInput.value = "";
  chatEl.scrollTop = chatEl.scrollHeight;
});

// Allow pressing Enter to ask question
qInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    askBtn.click();
  }
});