
function deleteRecipe(type, filename, btn) {
    if (!confirm('确定要删除该菜谱吗？')) return;
    fetch('/delete_recipe', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type, filename})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // 删除成功，移除该li
            btn.parentElement.remove();
        } else {
            alert('删除失败：' + data.message);
        }
    })
    .catch(() => alert('请求失败'));
}
function clearHistory() {
    if (!confirm('确定要清空所有历史记录吗？')) return;
    fetch('/clear_history', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // 找到所有section，找到包含“历史记录”按钮的那个
            const sections = document.querySelectorAll('.section');
            let historySection = null;
            sections.forEach(section => {
                const h2 = section.querySelector('h2');
                if (h2 && h2.textContent.includes('历史记录')) {
                    historySection = section;
                }
            });
            if (historySection) {
                const list = historySection.querySelector('.recipe-list');
                if (list) list.innerHTML = '';
                // 移除已有 empty-message
                const oldMsg = historySection.querySelector('.empty-message');
                if (oldMsg) oldMsg.remove();
                // 添加新的 empty-message
                const emptyMsg = document.createElement('div');
                emptyMsg.className = 'empty-message';
                emptyMsg.innerText = '暂无历史记录';
                historySection.appendChild(emptyMsg);
            }
        } else {
            alert('清空失败：' + data.message);
        }
    })
    .catch(() => alert('请求失败'));
}