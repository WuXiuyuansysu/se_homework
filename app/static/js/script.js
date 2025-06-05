// 存储菜谱数据的全局变量
let currentRecipeData = null;

// 当DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 烹饪风格选择框和输入框的切换逻辑
    const selectEl = document.getElementById('cuisine_type_select');
    const inputEl = document.getElementById('cuisine_type_input');
    const hiddenEl = document.getElementById('cuisine_type');
    
    // 当选择下拉选项时
    selectEl.addEventListener('change', function() {
        if(this.value) {
            inputEl.value = '';
            hiddenEl.value = this.value;
        }
    });
    
    // 当输入自定义内容时
    inputEl.addEventListener('input', function() {
        if(this.value) {
            selectEl.value = '';
            hiddenEl.value = this.value;
        }
    });
    
    // 表单提交事件监听
    document.querySelector('form').addEventListener('submit', async function(e) {
        // 先验证烹饪风格
        if (!hiddenEl.value) {
            e.preventDefault();
            alert('请选择或输入烹饪风格');
            inputEl.focus();
            return;
        }

        // 生成菜谱逻辑
        e.preventDefault();
        
        const formData = new FormData(this);
        const loading = document.getElementById('loading');
        const resultContainer = document.getElementById('result-container');
        
        try {
            // 显示加载动画
            loading.style.display = 'flex';
            resultContainer.style.display = 'none';

            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.error) throw new Error(data.error);
            
            // 存储菜谱数据用于导出
            currentRecipeData = data;

            // 构建结果HTML（添加导出按钮区域）
            const html = `
                <div class="export-buttons">
                    <button class="export-btn" id="export-txt">📝 导出为TXT</button>
                    <button class="export-btn" id="export-dish-png">🖼️ 导出主菜图片</button>
                    <button class="export-btn" id="export-steps-zip">📚 导出步骤图片包</button>
                </div>
                <div class="recipe-content">
                    <div class="recipe-header">
                        <h2>${data.recipe.name}</h2>
                        
                        <!-- 菜品图片展示 -->
                        <div class="dish-image-container">
                            <img src="data:image/png;base64,${data.dish_image}" 
                                 alt="${data.recipe.name}" 
                                 class="dish-image">
                            <p class="dish-description">${data.dish_description}</p>
                        </div>
                        
                        <div class="recipe-meta">
                            <div class="meta-item">
                                <span class="meta-icon">⏱</span>
                                <span>总时长：${data.recipe.total_time}</span>
                            </div>
                        </div>
                    </div>

                    <div class="section">
                        <h3>所需材料</h3>
                        <div class="ingredient-grid">
                            ${data.recipe.ingredients.map(i => `
                                <div class="ingredient-card">
                                    <strong>${i.name}</strong>
                                    <div>${i.quantity}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <div class="section">
                        <h3>烹饪步骤</h3>
                        <ol class="step-list">
                            ${data.recipe.steps.map((s, index) => `
                                <li class="step-item">
                                    <!-- 步骤图片 -->
                                    ${data.steps_images[index] ? `
                                        <div class="step-image-container">
                                            <img src="data:image/png;base64,${data.steps_images[index]}" 
                                                 alt="步骤 ${index + 1}" 
                                                 class="step-image">
                                        </div>
                                    ` : ''}
                                    
                                    ${s.description}
                                    <span class="step-duration">${s.duration}</span>
                                </li>
                            `).join('')}
                        </ol>
                    </div>
                </div>
            `;

            resultContainer.innerHTML = html;
            resultContainer.style.display = 'block';
            
            // 添加导出功能的事件监听
            document.getElementById('export-txt').addEventListener('click', exportRecipeAsTxt);
            document.getElementById('export-dish-png').addEventListener('click', exportDishImage);
            document.getElementById('export-steps-zip').addEventListener('click', exportStepsAsZip);
            
        } catch (err) {
            alert('生成失败: ' + err.message);
        } finally {
            loading.style.display = 'none';
        }
    });
});

// 导出为TXT的函数
function exportRecipeAsTxt() {
    const recipeContent = document.querySelector('.recipe-content');
    // 创建一个临时元素来提取文本内容
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = recipeContent.innerHTML;
    
    // 移除所有图片元素（保留描述文本）
    const images = tempDiv.querySelectorAll('img');
    images.forEach(img => img.remove());
    
    // 提取纯文本内容
    const textContent = tempDiv.innerText || tempDiv.textContent;
    
    // 创建Blob对象并下载
    const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = '菜谱.txt';
    document.body.appendChild(a);
    a.click();
    
    // 清理
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
}

// 导出主菜图片
function exportDishImage() {
    if (!currentRecipeData || !currentRecipeData.dish_image) {
        alert('没有菜品图片可导出');
        return;
    }
    
    try {
        // 显示导出加载提示
        const exportLoading = document.getElementById('export-loading');
        const exportMessage = document.getElementById('export-message');
        exportMessage.textContent = '正在导出主菜图片...';
        exportLoading.style.display = 'flex';
        
        // 提取纯base64数据（去除前缀）
        const base64Data = currentRecipeData.dish_image.split(',')[1] || currentRecipeData.dish_image;
        
        // 从base64创建Blob
        const byteString = atob(base64Data);
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        const blob = new Blob([ab], { type: 'image/png' });
        
        // 创建下载链接
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentRecipeData.recipe.name || 'dish'}.png`;
        document.body.appendChild(a);
        a.click();
        
        // 清理
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            exportLoading.style.display = 'none';
        }, 100);
    } catch (e) {
        alert('导出图片失败: ' + e.message);
        document.getElementById('export-loading').style.display = 'none';
    }
}

// 导出步骤图片为ZIP
function exportStepsAsZip() {
    if (!currentRecipeData || !currentRecipeData.steps_images || currentRecipeData.steps_images.length === 0) {
        alert('没有步骤图片可导出');
        return;
    }
    
    try {
        // 显示导出加载提示
        const exportLoading = document.getElementById('export-loading');
        const exportMessage = document.getElementById('export-message');
        exportMessage.textContent = '正在打包步骤图片...';
        exportLoading.style.display = 'flex';
        
        // 检查是否已加载JSZip库
        if (typeof JSZip === 'undefined') {
            // 动态加载JSZip库
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js';
            document.head.appendChild(script);
            
            script.onload = () => {
                createStepsZip();
            };
            script.onerror = () => {
                alert('加载JSZip库失败，请检查网络连接');
                exportLoading.style.display = 'none';
            };
        } else {
            createStepsZip();
        }
    } catch (e) {
        alert('导出失败: ' + e.message);
        document.getElementById('export-loading').style.display = 'none';
    }
}

// 创建步骤图片ZIP文件
function createStepsZip() {
    const exportLoading = document.getElementById('export-loading');
    const exportMessage = document.getElementById('export-message');
    
    try {
        const zip = new JSZip();
        const imgFolder = zip.folder('烹饪步骤');
        let validImages = 0;
        
        // 添加步骤图片到ZIP
        currentRecipeData.steps_images.forEach((imgData, index) => {
            if (!imgData) return;
            
            try {
                // 提取纯base64数据（去除前缀）
                const base64Data = imgData.split(',')[1] || imgData;
                
                // 从base64创建Blob
                const byteString = atob(base64Data);
                const ab = new ArrayBuffer(byteString.length);
                const ia = new Uint8Array(ab);
                for (let i = 0; i < byteString.length; i++) {
                    ia[i] = byteString.charCodeAt(i);
                }
                
                // 添加到ZIP
                imgFolder.file(`步骤${index + 1}.png`, ab);
                validImages++;
            } catch (e) {
                console.error(`步骤${index + 1}图片处理失败:`, e);
            }
        });
        
        if (validImages === 0) {
            throw new Error('没有有效的步骤图片');
        }
        
        exportMessage.textContent = '正在压缩图片包...';
        
        // 生成ZIP并下载
        zip.generateAsync({ type: 'blob' }).then(content => {
            const url = URL.createObjectURL(content);
            const a = document.createElement('a');
            a.href = url;
            a.download = '烹饪步骤.zip';
            document.body.appendChild(a);
            a.click();
            
            // 清理
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                exportLoading.style.display = 'none';
            }, 100);
        }).catch(e => {
            throw new Error('创建ZIP文件失败: ' + e.message);
        });
    } catch (err) {
        alert('导出失败: ' + err.message);
        exportLoading.style.display = 'none';
    }
}