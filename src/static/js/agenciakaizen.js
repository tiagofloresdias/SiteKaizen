// Agência Kaizen - JavaScript Personalizado

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initSmoothScrolling();
    initAnimations();
    initContactForm();
    initPortfolioFilters();
    initBlogSearch();
    initCountUpMetrics();
});

// Smooth Scrolling para links internos
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Animações de entrada
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    const animatedElements = document.querySelectorAll('.service-card, .portfolio-item, .blog-post');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
}

// Formulário de contato
function initContactForm() {
    const contactForm = document.querySelector('#contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            // Mostrar loading
            submitBtn.textContent = 'Enviando...';
            submitBtn.disabled = true;
            this.classList.add('loading');
            
            // Simular envio (substituir por chamada real)
            setTimeout(() => {
                // Mostrar sucesso
                showNotification('Mensagem enviada com sucesso!', 'success');
                
                // Resetar formulário
                this.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                this.classList.remove('loading');
            }, 2000);
        });
    }
}

// Filtros do portfolio
function initPortfolioFilters() {
    const filterButtons = document.querySelectorAll('.portfolio-filter');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // Atualizar botões ativos
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filtrar itens
            portfolioItems.forEach(item => {
                if (filter === 'all' || item.classList.contains(filter)) {
                    item.style.display = 'block';
                    item.classList.add('fade-in-up');
                } else {
                    item.style.display = 'none';
                    item.classList.remove('fade-in-up');
                }
            });
        });
    });
}

// Busca do blog
function initBlogSearch() {
    const searchInput = document.querySelector('#blog-search');
    const searchResults = document.querySelector('#search-results');
    
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 3) {
                searchResults.innerHTML = '';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                performBlogSearch(query);
            }, 300);
        });
    }
}

// Realizar busca no blog
function performBlogSearch(query) {
    // Simular busca (substituir por chamada real)
    const mockResults = [
        { title: 'Como criar um site responsivo', excerpt: 'Dicas essenciais para desenvolvimento web...', url: '/blog/como-criar-site-responsivo/' },
        { title: 'Marketing Digital em 2024', excerpt: 'Tendências e estratégias para o próximo ano...', url: '/blog/marketing-digital-2024/' }
    ];
    
    const filteredResults = mockResults.filter(result => 
        result.title.toLowerCase().includes(query.toLowerCase()) ||
        result.excerpt.toLowerCase().includes(query.toLowerCase())
    );
    
    displaySearchResults(filteredResults);
}

// Exibir resultados da busca
function displaySearchResults(results) {
    const searchResults = document.querySelector('#search-results');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<p class="text-muted">Nenhum resultado encontrado.</p>';
        return;
    }
    
    const html = results.map(result => `
        <div class="search-result-item p-3 border-bottom">
            <h6 class="mb-2">
                <a href="${result.url}" class="text-decoration-none">${result.title}</a>
            </h6>
            <p class="text-muted small mb-0">${result.excerpt}</p>
        </div>
    `).join('');
    
    searchResults.innerHTML = html;
}

// Mostrar notificações
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 1060; min-width: 300px;';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Remover automaticamente após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Count-up para métricas
function initCountUpMetrics(){
    const elements = document.querySelectorAll('.kaizen-count');
    if(elements.length === 0) return;

    const animate = (el) => {
        const targetRaw = (el.getAttribute('data-count-to')||'0').replace(/[^0-9.]/g,'');
        const suffix = el.getAttribute('data-suffix')||'';
        const target = parseFloat(targetRaw || '0');
        const duration = 1400; // ms
        const start = performance.now();

        const step = (now)=>{
            const progress = Math.min((now - start)/duration, 1);
            const current = Math.floor(target * progress);
            el.textContent = current.toLocaleString('pt-BR') + (suffix||'');
            if(progress < 1){ requestAnimationFrame(step); }
        };
        requestAnimationFrame(step);
    };

    const io = new IntersectionObserver((entries)=>{
        entries.forEach(entry=>{
            if(entry.isIntersecting){
                animate(entry.target);
                io.unobserve(entry.target);
            }
        })
    }, {threshold:0.3});

    elements.forEach(el=>io.observe(el));
}

// Lazy loading para imagens
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Utilitários
const Utils = {
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Formatar data
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('pt-BR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    // Validar email
    isValidEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
};

// Exportar para uso global
window.AgenciaKaizen = {
    Utils,
    showNotification
};
