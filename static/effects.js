// 初始化节日效果
function initFestival() {
    // 动态生成灯笼
    const container = document.querySelector('.lanterns');
    for (let i = 0; i < 6; i++) {
        const lantern = document.createElement('div');
        lantern.className = 'lantern';
        lantern.textContent = '🏮';
        lantern.style.left = `${Math.random() * 100}%`;
        lantern.style.animationDelay = `${Math.random() * 3}s`;
        container.appendChild(lantern);
    }

    // 点击烟花效果
    document.addEventListener('click', (e) => {
        const spark = document.createElement('div');
        spark.style.cssText = `
            position: absolute;
            left: ${e.clientX}px;
            top: ${e.clientY}px;
            width: 10px;
            height: 10px;
            background: radial-gradient(circle, #ffeb3b 30%, transparent 70%);
            animation: spark 0.8s linear;
        `;
        document.body.appendChild(spark);
        setTimeout(() => spark.remove(), 800);
    });
}

// 重试功能
function retry() {
    const input = document.querySelector('input[name="answer"]');
    if (input) {
        input.focus();
        input.select();
    }
}

// 启动
document.addEventListener('DOMContentLoaded', initFestival);
