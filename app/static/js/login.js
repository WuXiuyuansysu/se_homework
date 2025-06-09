document.addEventListener('DOMContentLoaded', () => {
    // 切换表单显示
    document.getElementById('show-register').addEventListener('click', () => {
        document.getElementById('login-form').classList.remove('active');
        document.getElementById('register-form').classList.add('active');
        clearMessage();
    });
    
    document.getElementById('show-login').addEventListener('click', () => {
        document.getElementById('register-form').classList.remove('active');
        document.getElementById('login-form').classList.add('active');
        clearMessage();
    });
    
    // 登录按钮事件
    document.getElementById('login-btn').addEventListener('click', () => {
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        
        if (!username || !password) {
            showMessage('请填写用户名和密码', 'error');
            return;
        }
        
        login(username, password);
    });
    
    // 注册按钮事件
    document.getElementById('register-btn').addEventListener('click', () => {
        const username = document.getElementById('register-username').value;
        const password = document.getElementById('register-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
        
        if (!username || !password || !confirmPassword) {
            showMessage('请填写所有字段', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            showMessage('两次输入的密码不一致', 'error');
            return;
        }
        
        register(username, password);
    });
});

function login(username, password) {
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&action=login`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            // 登录成功后跳转到主页
            setTimeout(() => {
                window.location.href = '/index';
            }, 1500);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('网络错误，请重试', 'error');
        console.error('登录错误:', error);
    });
}

function register(username, password) {
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&action=register`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            // 注册成功后自动登录并跳转
            setTimeout(() => {
                window.location.href = '/index';
            }, 1500);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('网络错误，请重试', 'error');
        console.error('注册错误:', error);
    });
}

function showMessage(message, type) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
    
    // 3秒后自动隐藏消息
    setTimeout(clearMessage, 3000);
}

function clearMessage() {
    const messageEl = document.getElementById('message');
    messageEl.textContent = '';
    messageEl.className = 'message';
}