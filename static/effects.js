// 初始化特效
document.addEventListener('DOMContentLoaded', () => {
    // 创建动态灯笼
    createLanterns(5);
    
    // 表单提交特效
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if(this.checkValidity()) {
                createFireworks();
                // 添加成功反馈
                if(this.action.includes('/add')) {
                    const btn = this.querySelector('button');
                    btn.innerHTML = '✔ 添加成功';
                    setTimeout(() => btn.innerHTML = '✨ 提交灯谜', 1500);
                }
            }
        });
    });
});

// 创建灯笼
function createLanterns(count = 3) {
    const container = document.querySelector('.lanterns');
    const colors = ['#e74c3c', '#f1c40f', '#2ecc71'];
    
    for(let i = 0; i < count; i++) {
        const lantern = document.createElement('div');
        lantern.className = `lantern ${i%2 ? 'swing' : 'swing-delay'}`;
        lantern.style.cssText = `
            left: ${Math.random() * 90}%;
            top: ${Math.random() * 80}%;
            width: ${Math.random() * 40 + 30}px;
            background: ${colors[Math.floor(Math.random()*colors.length)]};
            opacity: 0.8;
        `;
        container.appendChild(lantern);
    }
}

// 创建烟花
function createFireworks() {
    const container = document.getElementById('fireworks');
    for(let i = 0; i < 8; i++) {
        const particle = document.createElement('div');
        particle.className = 'firework-particle';
        particle.style.cssText = `
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            background: hsl(${Math.random()*360}, 70%, 50%);
            animation: explode 1s ease-out;
        `;
        container.appendChild(particle);
        setTimeout(() => particle.remove(), 1000);
    }
}
