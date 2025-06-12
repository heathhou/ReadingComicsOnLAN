document.addEventListener('DOMContentLoaded', () => {
    const fileList = document.getElementById('file-list');
    const breadcrumb = document.getElementById('breadcrumb');
    const includeSubfoldersCheckbox = document.getElementById('include-subfolders');

    // 从URL或localStorage获取当前路径
    const urlParams = new URLSearchParams(window.location.search);
    let currentPath = urlParams.get('path') || '';

    // 从localStorage加载复选框状态
    const shouldIncludeSubfolders = localStorage.getItem('includeSubfolders') === 'true';
    includeSubfoldersCheckbox.checked = shouldIncludeSubfolders;

    includeSubfoldersCheckbox.addEventListener('change', () => {
        localStorage.setItem('includeSubfolders', includeSubfoldersCheckbox.checked);
    });

    async function fetchAndDisplayFiles(path) {
        try {
            const response = await fetch(`/api/list?path=${encodeURIComponent(path)}`);
            if (!response.ok) {
                throw new Error('无法加载文件列表');
            }
            const data = await response.json();

            // 如果文件夹只包含图片（没有子文件夹），则直接打开阅读器
            if (data.folders.length === 0 && data.images.length > 0) {
                const includeSubfolders = document.getElementById('include-subfolders').checked;
                // 在当前标签页中打开垂直阅读模式
                window.location.href = `/reader?path=${encodeURIComponent(path)}&mode=vertical&subfolders=${includeSubfolders}`;
                return; // 阻止后续代码执行，以防页面刷新
            }

            // 对于包含子文件夹或为空的目录，则正常显示其内容
            currentPath = data.path;
            updateBreadcrumb(data.path);
            renderFileList(data.folders, data.images, data.path);
            // 更新URL
            const newUrl = `${window.location.pathname}?path=${encodeURIComponent(currentPath)}`;
            window.history.pushState({path: currentPath}, '', newUrl);

        } catch (error) {
            fileList.innerHTML = `<p>${error.message}</p>`;
        }
    }

    function renderFileList(folders, images, path) {
        fileList.innerHTML = '';
        if (folders.length === 0 && images.length === 0) {
            fileList.innerHTML = '<p>这个文件夹是空的。</p>';
            return;
        }

        folders.forEach(folder => {
            const item = createFolderItem(folder, path);
            fileList.appendChild(item);
        });

        // 在主页不直接显示图片，只显示文件夹
        // images.forEach(image => {
        //     const item = createImageItem(image, path);
        //     fileList.appendChild(item);
        // });
    }
    
    function createFolderItem(name, currentPath) {
        const item = document.createElement('div');
        item.className = 'file-item';
        const fullPath = currentPath ? `${currentPath}/${name}` : name;

        item.innerHTML = `
            <div class="item-info" title="${name}">
                <div class="folder-icon">📁</div>
                <div class="item-name">${name}</div>
            </div>
            <div class="item-actions">
                <button onclick="event.stopPropagation(); openReader('${fullPath}', 'vertical')">垂</button>
                <button onclick="event.stopPropagation(); openReader('${fullPath}', 'horizontal')">平</button>
            </div>
        `;
        
        item.addEventListener('click', () => fetchAndDisplayFiles(fullPath));
        
        return item;
    }

    function updateBreadcrumb(path) {
        breadcrumb.innerHTML = '';
        const homeLink = document.createElement('a');
        homeLink.href = '#';
        homeLink.textContent = '根目录';
        homeLink.addEventListener('click', (e) => {
            e.preventDefault();
            fetchAndDisplayFiles('');
        });
        breadcrumb.appendChild(homeLink);

        if (path) {
            const parts = path.split('/');
            let current = '';
            parts.forEach((part, index) => {
                current += (index > 0 ? '/' : '') + part;
                const span = document.createElement('span');
                span.textContent = ' > ';
                breadcrumb.appendChild(span);

                const partLink = document.createElement('a');
                partLink.href = '#';
                partLink.textContent = part;
                const pathToFetch = current; // 闭包问题
                partLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    fetchAndDisplayFiles(pathToFetch);
                });
                breadcrumb.appendChild(partLink);
            });
        }
    }
    
    // History API a back/forward navigation
    window.addEventListener('popstate', (event) => {
        if (event.state && event.state.path !== undefined) {
            fetchAndDisplayFiles(event.state.path);
        } else {
            fetchAndDisplayFiles(''); // Fallback to root
        }
    });

    // Initial load
    fetchAndDisplayFiles(currentPath);
});

function openReader(path, mode) {
    const includeSubfolders = document.getElementById('include-subfolders').checked;
    window.open(`/reader?path=${encodeURIComponent(path)}&mode=${mode}&subfolders=${includeSubfolders}`, '_blank');
}
