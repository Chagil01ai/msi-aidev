const spinner = document.getElementById('spinner');
const chatBox = document.getElementById('chatBox');
let conversation = [];

function appendMessage(text, role) {
  const div = document.createElement('div');
  div.className = `bubble ${role}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function askClaude() {
  const inputField = document.getElementById('userInput');
  const userInput = inputField.value.trim();
  if (!userInput) return;

  appendMessage(userInput, 'user');
  inputField.value = '';
  spinner.style.display = 'inline-block';

  conversation.push({ role: "user", content: userInput });

  const response = await fetch('/stream_claude', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ history: conversation })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let assistantText = '';
  let div = document.createElement('div');
  div.className = 'bubble assistant';
  chatBox.appendChild(div);

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value);
    const match = chunk.match(/data: (.*)/);
    if (match) {
      const text = match[1];
      assistantText += text;
      div.textContent = assistantText;
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }

  spinner.style.display = 'none';
  conversation.push({ role: "assistant", content: assistantText });
}
