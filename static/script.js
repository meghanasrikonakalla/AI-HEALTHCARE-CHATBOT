// static/script.js
const chatBox = document.getElementById('chat-box');
const input   = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const restartBtn = document.getElementById('restart-btn');

// Add typing indicator
function showTypingIndicator() {
  const indicator = document.createElement('div');
  indicator.classList.add('typing-indicator');
  indicator.innerHTML = `
    <div class="typing-dots">
      <span></span>
      <span></span>
      <span></span>
    </div>
    <span style="margin-left: 8px;">Healthcare AI is thinking...</span>
  `;
  indicator.id = 'typing-indicator';
  chatBox.appendChild(indicator);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTypingIndicator() {
  const indicator = document.getElementById('typing-indicator');
  if (indicator) {
    indicator.remove();
  }
}

function appendMessage(text, sender) {
  const msg = document.createElement('div');
  msg.classList.add('message', sender);

  if (sender === 'bot') {
    // text contains HTML (safe-sanitized below)
    msg.innerHTML = text;
  } else {
    // user text must remain plain text
    msg.textContent = text;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * sanitizeHTML - light sanitizer: allow only a small whitelist of tags,
 * and strip attributes. This avoids loading external libs while preventing
 * most injection risks.
 */
function sanitizeHTML(dirty) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(dirty, 'text/html');

  const whitelist = new Set(['BR','B','STRONG','I','EM','U','UL','OL','LI','P']);

  function clean(node) {
    // make a static copy because we'll mutate the DOM
    const children = Array.from(node.childNodes);
    for (const child of children) {
      if (child.nodeType === Node.ELEMENT_NODE) {
        if (!whitelist.has(child.tagName)) {
          // unwrap element: replace element with its children
          const frag = document.createDocumentFragment();
          while (child.firstChild) frag.appendChild(child.firstChild);
          node.replaceChild(frag, child);
          // continue cleaning the new children inside frag
        } else {
          // remove all attributes on allowed tags
          for (const attr of Array.from(child.attributes)) child.removeAttribute(attr.name);
          clean(child); // recursive
        }
      } else if (child.nodeType === Node.TEXT_NODE) {
        // keep text nodes
      } else {
        // remove comment nodes, processing instructions etc
        node.removeChild(child);
      }
    }
  }

  clean(doc.body);
  return doc.body.innerHTML;
}

/** sendMessage: main flow */
async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  appendMessage(text, 'user');
  input.value = '';
  
  // Show typing indicator
  showTypingIndicator();

  console.log('→ Sending to /chat:', text);

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    // Hide typing indicator
    hideTypingIndicator();

    if (!res.ok) {
      // show status and try to read body for debug
      const t = await res.text().catch(()=>'');
      console.error('Network response not ok', res.status, t);
      appendMessage('⚠️ Server returned status ' + res.status, 'bot');
      return;
    }

    let data;
    try {
      data = await res.json();
      console.log('← JSON received:', data);
    } catch (err) {
      // If not JSON, try plain text
      const txt = await res.text();
      console.warn('← Non-JSON response, fallback to text:', txt);
      data = { reply: txt };
    }

    // support several possible keys
    let replyRaw = '';
    if (typeof data === 'string') replyRaw = data;
    else if (data.reply) replyRaw = data.reply;
    else if (data.bot) replyRaw = data.bot;
    else if (data.message) replyRaw = data.message;
    else replyRaw = JSON.stringify(data);

    // If server returned plain newlines, convert them to <br>
    replyRaw = String(replyRaw).replace(/\r\n/g, '\n').replace(/\n/g, '<br>');

    // sanitize but keep allowed tags
    const safe = sanitizeHTML(replyRaw);

    appendMessage(safe, 'bot');

  } catch (err) {
    hideTypingIndicator();
    console.error('Fetch error:', err);
    appendMessage('⚠️ Network or server error. Please check your connection and try again.', 'bot');
  }
}

// Restart consultation function
async function restartConsultation() {
  try {
    const res = await fetch('/restart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    if (res.ok) {
      // Clear chat box except welcome message
      const welcomeMsg = document.querySelector('.welcome-message');
      chatBox.innerHTML = '';
      if (welcomeMsg) {
        chatBox.appendChild(welcomeMsg.cloneNode(true));
      }
      
      const data = await res.json();
      appendMessage(data.reply, 'bot');
    }
  } catch (err) {
    console.error('Restart error:', err);
    appendMessage('⚠️ Error restarting consultation.', 'bot');
  }
}

sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });
restartBtn.addEventListener('click', restartConsultation);

// Auto-focus input field
input.focus();
