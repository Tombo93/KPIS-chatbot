const threadEl = document.getElementById('thread');
const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');
const stopBtn = document.getElementById('stopBtn');
const themeToggle = document.getElementById('themeToggle');
const usageEl = document.getElementById('usage');

let controller = null;

// Helpers
function escapeHTML(str) {
    const p = document.createElement('p');
    p.textContent = str;
    return p.innerHTML;
}

function addMessage(role, html) {
    const msg = document.createElement('div');
    msg.className = `message ${role}`;
    msg.innerHTML = `
        <div class="avatar">${role === 'user' ? 'You' : 'AI'}</div>
        <div class="bubble">${html}
          <div class="meta">
            <span>${role === 'user' ? 'You' : 'Copilot'}</span>
            ${role === 'ai' ? '<span class="status"><span class="dot"></span>Thinking</span>' : ''}
          </div>
        </div>
      `;
    threadEl.appendChild(msg);
    msg.scrollIntoView({ behavior: 'smooth', block: 'end' });
    return msg;
}

function updateUsage(chars) {
    usageEl.textContent = String(chars);
}

async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;
    inputEl.value = '';
    updateUsage(0);

    addMessage('user', escapeHTML(text));
    const aiMsg = addMessage('ai', '');

    sendBtn.disabled = true;
    stopBtn.disabled = false;
    controller = new AbortController();

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text }),
            signal: controller.signal
        });

        if (!res.ok) {
            throw new Error('Network response was not ok');
        }

        // Stream response if server uses text/event-stream or chunked text
        const reader = res.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            // Simple chunk parser: split on newline boundaries
            const parts = buffer.split('\n');
            buffer = parts.pop(); // keep incomplete tail
            for (const chunk of parts) {
                if (!chunk) continue;
                // Expect raw text chunks or JSON lines like: {"delta":"...","usage":123}
                try {
                    const obj = JSON.parse(chunk);
                    if (obj.delta) {
                        aiMsg.querySelector('.bubble').insertAdjacentHTML('beforeend', escapeHTML(obj.delta));
                    }
                    if (obj.usage != null) {
                        updateUsage(obj.usage);
                    }
                } catch {
                    // treat as plain text
                    aiMsg.querySelector('.bubble').insertAdjacentHTML('beforeend', escapeHTML(chunk));
                }
                aiMsg.querySelector('.status')?.remove();
                aiMsg.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }
        }
    } catch (err) {
        aiMsg.querySelector('.bubble').insertAdjacentHTML(
            'beforeend',
            `<div class="meta" style="color: var(--danger)">Error: ${escapeHTML(err.message)}</div>`
        );
    } finally {
        sendBtn.disabled = false;
        stopBtn.disabled = true;
        controller = null;
    }
}

sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

stopBtn.addEventListener('click', () => {
    if (controller) controller.abort();
    stopBtn.disabled = true;
    sendBtn.disabled = false;
});

document.querySelectorAll('[data-suggestion]').forEach(btn => {
    btn.addEventListener('click', () => {
        inputEl.value = btn.dataset.suggestion;
        inputEl.focus();
    });
});

themeToggle.addEventListener('click', () => {
    const html = document.documentElement;
    html.setAttribute('data-theme', html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
});