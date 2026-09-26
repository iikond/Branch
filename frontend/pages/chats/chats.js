    let wsHost = '';
    
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        wsHost = 'localhost';
    } else {
        wsHost = window.location.hostname;
    }
    
    const wsUrl = `ws://${wsHost}:8000/ws/chat`;
    const ws = new WebSocket(wsUrl);
    const messagesDiv = document.getElementById('messages');
    const statusDiv = document.getElementById('status');
    const input = document.getElementById('message-input');

    ws.onopen = () => {
        console.log('✅ Подключено к WebSocket');
        statusDiv.textContent = '🟢 Подключено';
        statusDiv.style.background = '#d4edda';
        input.focus();
    };

    ws.onmessage = (event) => {
        addMessage(event.data, 'user');
        console.log('📩 Получено:', event.data);
    };

    ws.onerror = () => {
        console.error('❌ Ошибка WebSocket');
        statusDiv.textContent = '🔴 Ошибка подключения к серверу';
        statusDiv.style.background = '#f8d7da';
    };

    ws.onclose = () => {
        console.log('⚠️ Отключено (обновите страницу)');
        statusDiv.textContent = '🔴 Отключено (запустите бэкенд и обновите)';
        statusDiv.style.background = '#f8d7da';
    };

    function addMessage(text, type) {
        const div = document.createElement('div');
        div.className = 'message ' + type;
        div.textContent = text.trim();
        messagesDiv.appendChild(div);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function sendMessage() {
        if (!ws || ws.readyState !== WebSocket.OPEN) return alert('Не подключено!');
        
        const msg = input.value.trim();
        if (!msg) return;
        
        input.value = '';
        ws.send(msg);
    }

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });