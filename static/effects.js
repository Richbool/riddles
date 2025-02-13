function handleSubmit(form) {
    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.innerHTML = '<div class="loader"></div> 校验中...';
    
    // 清理旧结果
    document.querySelectorAll('.result').forEach(el => el.remove());
}

function lockForm(form) {
    form.querySelector('button').disabled = true;
}

function showLoader() {
    const btn = document.querySelector('.btn');
    if (btn) {
        btn.innerHTML = '<div class="loader"></div> 加载中...';
    }
}

// 防止重复提交
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', () => {
            form.querySelector('button').disabled = true;
        });
    });
});
