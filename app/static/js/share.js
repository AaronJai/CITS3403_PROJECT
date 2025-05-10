// Share carbon emissions data with user
function shareWith(email) {
    fetch('/api/share', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
    })
        .then(res => res.json())
        .then(() => {
            window.location.href = '/share';
        });
}

// Generate a preview card for the shared user
function generatePreviewCard({ name, email, travel_pct, food_pct, home_pct, shopping_pct, total_emission }) {
    return `
<tr id="preview-${email}">
    <td colspan="5">
        <section class="mt-2">
            <div class="bg-white p-4 rounded-md">
                <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <div class="grid grid-cols-2 gap-4">
                        ${['Travel', 'Home', 'Food', 'Shopping'].map((label, i) => {
                            let percent = [travel_pct, home_pct, food_pct, shopping_pct][i];
                            const cappedPercent = Math.min(percent, 100); // Cap at 100%
                            return `
                            <div class="bg-white p-3 rounded-md shadow-sm">
                                <h3 class="font-semibold">${label}</h3>
                                <div class="mt-2 h-2 bg-gray-200 rounded-full">
                                    <div class="h-2 bg-primary rounded-full" style="width: ${cappedPercent}%"></div>
                                </div>
                                <p class="text-sm text-gray-600 mt-1"><strong>${percent}%</strong> of their carbon budget</p>
                            </div>`;
                        }).join('')}
                    </div>
                    <p class="mt-4 text-sm font-semibold text-center">
                        Total: <span class="text-primary">${total_emission.toFixed(2)}kg CO2eq</span> this month
                    </p>
                </div>
            </div>
        </section>
    </td>
</tr>
    `;
}

// Toggle shared user emissions - show or hide the preview card
function toggleSharedUserEmissions(email) {
    // Check if the preview already exists
    const existingPreview = document.getElementById(`preview-${email}`);
    // Remove highlight from all rows first
    document.querySelectorAll('tr[data-email]').forEach(row => {
        row.classList.remove('bg-gray-100');
    });
    if (existingPreview) {
        // If preview exists, remove it (close)
        existingPreview.remove();
    } else {
        // If preview doesn't exist, load and show it (open)
        loadSharedUserEmissions(email);
        // Highlight the toggled row
        const userRow = document.querySelector(`tr[data-email="${email}"]`);
        if (userRow) {
            userRow.classList.add('bg-gray-100');
        }
    }
}

// Load shared user emissions and display them in a preview card
function loadSharedUserEmissions(email) {
    fetch(`/api/emissions/${email}`)
        .then(res => res.json())
        .then(data => {
            document.querySelectorAll('[id^="preview-"]').forEach(row => row.remove());

            const previewHtml = generatePreviewCard({
                name: data.name || 'Unknown',
                email,
                travel_pct: data.travel_pct,
                food_pct: data.food_pct,
                home_pct: data.home_pct,
                shopping_pct: data.shopping_pct,
                total_emission: data.total_emissions
            });

            const userRow = document.querySelector(`tr[data-email="${email}"]`);
            if (userRow) {
                userRow.insertAdjacentHTML('afterend', previewHtml);
            }
        })
        .catch(error => {
            console.error('Error loading shared emissions:', error);
        });
}

let chattingWith = null;

// Start a chat with a user
function startChat(email) {
    console.log("Starting chat with:", email);
    chattingWith = email;
    document.getElementById('chatTitle').innerText = "Chat with " + email;
    document.getElementById('chatBox').classList.remove('hidden');
    loadMessages();
    const dot = document.getElementById(`dot-${email}`);
  if (dot) {
    dot.remove();
  }
}

// Close the chat
function closeChat() {
    document.getElementById('chatBox').classList.add('hidden');
    chattingWith = null;
}

// Send a chat message
function sendMessage(event) {
    event.preventDefault();
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message || !chattingWith) return;

    console.log("Sending message:", message, "to", chattingWith);

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ to: chattingWith, message: message })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                appendMessage('You', message);
                input.value = '';                
                loadMessages();                  
            } else {
                alert("Failed to send: " + data.error);
            }
        })
        .catch(err => {
            console.error("Failed to send:", err);
        });
}

// Append a chat message to the chat box
function appendMessage(sender, message) {
    const box = document.getElementById('chatMessages');
    const isSelf = sender === 'You';  // Check if the message is sent by the user

    const messageWrapper = document.createElement('div');
    messageWrapper.className = `flex ${isSelf ? 'justify-end' : 'justify-start'}`;

    const bubble = document.createElement('div');
    bubble.className = 'max-w-[75%] px-4 py-2 rounded-xl text-sm bg-gray-200 text-gray-800 shadow';

    bubble.innerText = message; // Do not display the sender's name

    messageWrapper.appendChild(bubble);
    box.appendChild(messageWrapper);

    box.scrollTop = box.scrollHeight;
}

// Load chat messages
function loadMessages() {
    fetch(`/chat/${chattingWith}`)
        .then(res => res.json())
        .then(messages => {
            const box = document.getElementById('chatMessages');
            box.innerHTML = '';
            messages.forEach(msg => {
                appendMessage(msg.sender === currentUser ? 'You' : msg.sender, msg.content);
            });
        });
}

// Add event listener for sending messages on Enter key press
document.getElementById('chatInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.getElementById('chatForm').dispatchEvent(new Event('submit'));
    }
});
