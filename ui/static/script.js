/* ==========================================
   Document Summarizer - Frontend JavaScript
   ========================================== */

// API Base URL
const API_BASE = '/api';

// Helper to safely get elements
function el(id) {
    return document.getElementById(id);
}

// Tab switching
function switchTab(button, tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.nav-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    const target = document.getElementById(tabName);
    if (target) {
        target.classList.add('active');
    }

    // Add active class to clicked button (if provided)
    if (button && button.classList) {
        button.classList.add('active');
    }

    // Load history when history tab is clicked
    if (tabName === 'history') {
        loadHistory();
    }
}

// Notification system
function showNotification(message, type = 'info', duration = 3000) {
    const notif = document.getElementById('notification');
    notif.textContent = message;
    notif.className = `notification show ${type}`;
    
    setTimeout(() => {
        notif.classList.remove('show');
    }, duration);
}

// Note: input listeners are attached after DOMContentLoaded to avoid null refs
function updateTextInfo(text) {
    const wordCount = text.trim().split(/\s+/).filter(w => w.length > 0).length;
    const readingTime = Math.max(1, Math.ceil(wordCount / 200));
    
    const infoDiv = document.getElementById('textInfo');
    if (infoDiv) {
        infoDiv.innerHTML = `
            <span>Words: <strong>${wordCount}</strong></span>
            <span>Reading Time: <strong>${readingTime}</strong> min</span>
        `;
    }
}

// ==========================================
// SUMMARIZER FUNCTIONS
// ==========================================

async function summarizeText() {
    const text = document.getElementById('inputText').value.trim();
    const context = document.getElementById('contextInput').value.trim();
    
    if (!text) {
        showNotification('Please enter some text to summarize', 'error');
        return;
    }
    
    if (text.split(/\s+/).length < 20) {
        showNotification('Please enter at least 20 words', 'error');
        return;
    }
    
    const loading = document.getElementById('loadingIndicator');
    loading.style.display = 'block';
    
    try {
        const endpoint = context ? `${API_BASE}/summarize-context` : `${API_BASE}/summarize`;
        const payload = context ? { text, context } : { text };

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        console.log('Summarize API response:', data); // DEBUG

        if (response.ok) {
            displayResults(data);
            showNotification('Summary generated successfully!', 'success');
        } else {
            displayResults(data); // Show results section even on error for debug
            showNotification(data.error || 'Error generating summary', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error communicating with server', 'error');
        displayResults({ summary: '', error: error.toString() }); // Show results section on JS error
    } finally {
        loading.style.display = 'none';
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');

    // Display summary or error
    let summaryText = data.summary || '';
    if (data.error) {
        summaryText += `\n[Error: ${data.error}]`;
    }
    document.getElementById('summaryOutput').textContent = summaryText || 'No summary generated';

    // Display keywords
    const keywordsContainer = document.getElementById('keywordsOutput');
    keywordsContainer.innerHTML = (data.keywords || []).map(kw => 
        `<span class="keyword">${kw}</span>`
    ).join('');

    // Display statistics
    const stats = [
        `Original Text Length: ${data.original_length || 0} words`,
        `Summary Length: ${data.summary_length || 0} words`,
        `Compression Ratio: ${data.compression_ratio || 0}x`,
        `Context: ${document.getElementById('contextInput').value.trim() || 'None'}`
    ];

    document.getElementById('statsOutput').innerHTML = stats.map(stat => 
        `<li>${stat}</li>`
    ).join('');

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function clearSummarizer() {
    document.getElementById('inputText').value = '';
    document.getElementById('contextInput').value = '';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('textInfo').innerHTML = '<span>Words: <strong>0</strong></span><span>Reading Time: <strong>0</strong> min</span>';
}

function copySummary() {
    const summary = document.getElementById('summaryOutput').textContent;
    navigator.clipboard.writeText(summary).then(() => {
        showNotification('Summary copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy summary', 'error');
    });
}

function downloadSummary() {
    const summary = document.getElementById('summaryOutput').textContent;
    const text = document.getElementById('inputText').value;
    
    const content = `DOCUMENT SUMMARIZATION REPORT
============================

ORIGINAL TEXT (First 500 characters):
${text.substring(0, 500)}...

SUMMARY:
${summary}

Generated by Document Summarizer & Contextual Binding
`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `summary_${new Date().getTime()}.txt`;
    a.click();
    window.URL.revokeObjectURL(url);
    
    showNotification('Summary downloaded!', 'success');
}

// ==========================================
// CHATBOT FUNCTIONS
// ==========================================

async function loadChatbotDocument() {
    const text = document.getElementById('chatbotText').value.trim();
    
    if (!text) {
        showNotification('Please enter a document', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/chatbot/load`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            document.getElementById('chatInterface').style.display = 'block';
            document.getElementById('chatHistory').innerHTML = '';
            
            const statusDiv = document.getElementById('chatbotStatus');
            statusDiv.className = 'status-message success';
            statusDiv.innerHTML = `✓ Document loaded successfully! (${data.word_count} words, ${data.reading_time} min read)`;
            statusDiv.style.display = 'block';
            
            addChatMessage('assistant', 'Document loaded! I can now answer questions about it. What would you like to know?');
            
            showNotification('Document loaded successfully!', 'success');
        } else {
            showNotification(data.error || 'Error loading document', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error loading document', 'error');
    }
}

async function askQuestion() {
    const question = document.getElementById('chatQuestion').value.trim();
    
    if (!question) {
        showNotification('Please enter a question', 'error');
        return;
    }
    
    // Add user message to chat
    addChatMessage('user', question);
    document.getElementById('chatQuestion').value = '';
    
    try {
        const response = await fetch(`${API_BASE}/chatbot/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            let answer = data.answer;
            if (data.related_keywords && data.related_keywords.length > 0) {
                answer += `\n\n(Related concepts: ${data.related_keywords.join(', ')})`;
            }
            addChatMessage('assistant', answer);
        } else {
            addChatMessage('assistant', 'Sorry, I couldn\'t generate an answer. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        addChatMessage('assistant', 'Error communicating with the server.');
    }
}

function addChatMessage(role, message) {
    const chatHistory = document.getElementById('chatHistory');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble';
    bubble.textContent = message;
    
    messageDiv.appendChild(bubble);
    chatHistory.appendChild(messageDiv);
    
    // Scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function handleChatKeypress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        askQuestion();
    }
}

function unloadChatbot() {
    document.getElementById('chatInterface').style.display = 'none';
    document.getElementById('chatbotText').value = '';
    document.getElementById('chatHistory').innerHTML = '';
    document.getElementById('chatbotStatus').style.display = 'none';
}

// ==========================================
// HISTORY FUNCTIONS
// ==========================================

async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/history?limit=20`);
        const data = await response.json();
        
        if (response.ok) {
            displayHistory(data.history || []);
        } else {
            showNotification('Error loading history', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error loading history', 'error');
    }
}

function displayHistory(history) {
    const container = document.getElementById('historyContainer');
    
    if (history.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #718096; padding: 2rem;">No history yet. Start summarizing documents!</p>';
        return;
    }
    
    container.innerHTML = history.reverse().map((item, index) => `
        <div class="section-card history-item">
            <div class="timestamp">🕐 ${new Date(item.timestamp).toLocaleString()}</div>
            <div class="text">
                <strong>Original:</strong> ${item.original_text}...
            </div>
            <div class="text">
                <strong>Summary:</strong> ${item.summary.substring(0, 100)}...
            </div>
            ${item.keywords ? `
                <div class="keywords">
                    ${item.keywords.map(kw => `<span class="keyword-badge">${kw}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

async function searchHistory() {
    const keyword = document.getElementById('searchKeyword').value.trim();
    
    if (!keyword) {
        loadHistory();
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/history/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ keyword })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayHistory(data.results || []);
            showNotification(`Found ${(data.results || []).length} results`, 'info');
        } else {
            showNotification('Error searching history', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error searching history', 'error');
    }
}

async function clearAllHistory() {
    if (!confirm('Are you sure you want to clear all history? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/history/clear`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('historyContainer').innerHTML = '';
            document.getElementById('searchKeyword').value = '';
            showNotification('History cleared successfully', 'success');
        } else {
            showNotification('Error clearing history', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error clearing history', 'error');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document Summarizer loaded successfully!');

    // Attach text input listener safely
    const input = el('inputText');
    if (input) {
        input.addEventListener('input', (e) => updateTextInfo(e.target.value || ''));
        // initialize info display
        updateTextInfo(input.value || '');
    }

    // Attach chat question keypress handler if present
    const chatInput = el('chatQuestion');
    if (chatInput) {
        chatInput.addEventListener('keypress', handleChatKeypress);
    }
});
