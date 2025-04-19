const uploadEl = document.getElementById("pdf-upload");
const chatEl = document.getElementById("chat");
const qInput = document.getElementById("question");
const askBtn = document.getElementById("ask-btn");

const BACKEND = "http://localhost:8000";
let extractedText = null;

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
    extractedText = result.text;
    addMessage(`PDF "${result.filename}" uploaded successfully`, 'bot');
  } catch (error) {
    addMessage("Upload failed: " + error.message, 'error');
    console.error("Upload failed:", error);
  }
});

// 2) Ask question
askBtn.addEventListener("click", async () => {
  const question = qInput.value.trim();
  if (!question) return;
  
  if (!extractedText) {
    addMessage("Please upload a PDF first", 'error');
    return;
  }
  
  addMessage(question, 'you');
  
  try {
    const res = await fetch(`${BACKEND}/ask`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question: question,
        context: extractedText
      })
    });
    
    const result = await res.json();
    if (result.answer) {
      addMessage(result.answer, 'bot');
    } else {
      addMessage("No answer received", 'error');
    }
  } catch (error) {
    addMessage("Failed to get answer", 'error');
    console.error("Error:", error);
  }
  
  qInput.value = "";
  chatEl.scrollTop = chatEl.scrollHeight;
});

function addMessage(text, sender) {
  const messageEl = document.createElement('div');
  messageEl.classList.add('message', sender);
  messageEl.textContent = text;
  chatEl.appendChild(messageEl);
}

// Allow pressing Enter to ask question
qInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    askBtn.click();
  }
});