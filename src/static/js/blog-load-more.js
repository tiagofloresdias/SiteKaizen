/**
 * Sistema de Carregar Mais para Blog - Otimizado para SEO
 * Agência Kaizen
 */

class BlogLoadMore {
    constructor() {
        this.currentPage = 1;
        this.isLoading = false;
        this.hasMore = true;
        this.currentCategory = '';
        this.currentSearch = '';
        this.totalPosts = 0;
        
        this.init();
    }
    
    init() {
        this.loadMoreBtn = document.querySelector('.load-more-btn');
        this.postsContainer = document.querySelector('.blog-posts-grid');
        this.searchInput = document.querySelector('.blog-search-input');
        this.searchBtn = document.querySelector('.blog-search-btn');
        this.categoryFilter = document.querySelector('.category-filter');
        
        if (this.loadMoreBtn) {
            this.loadMoreBtn.addEventListener('click', () => this.loadMore());
        }
        
        if (this.searchBtn && this.searchInput) {
            this.searchBtn.addEventListener('click', () => this.searchPosts());
            this.searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.searchPosts();
                }
            });
        }
        
        if (this.categoryFilter) {
            this.categoryFilter.addEventListener('change', () => this.filterByCategory());
        }
        
        // Inicializar dados da primeira página
        this.initializeData();
    }
    
    initializeData() {
        // Obter dados iniciais do HTML
        const initialData = document.querySelector('[data-blog-data]');
        if (initialData) {
            try {
                const data = JSON.parse(initialData.textContent);
                this.currentPage = data.current_page || 1;
                this.hasMore = data.has_next || false;
                this.totalPosts = data.total_posts || 0;
            } catch (e) {
                console.warn('Erro ao carregar dados iniciais do blog:', e);
            }
        }
    }
    
    async loadMore() {
        if (this.isLoading || !this.hasMore) return;
        
        this.isLoading = true;
        this.updateLoadMoreButton(true);
        
        try {
            const nextPage = this.currentPage + 1;
            const params = new URLSearchParams({
                page: nextPage
            });
            
            if (this.currentCategory) {
                params.append('category', this.currentCategory);
            }
            
            if (this.currentSearch) {
                params.append('search', this.currentSearch);
            }
            
            const response = await fetch(`/aprenda-marketing-digital/api/load-more/?${params}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.appendPosts(data.html);
                this.currentPage = data.current_page;
                this.hasMore = data.has_next;
                this.totalPosts = data.total_posts;
                
                // Atualizar URL para SEO (sem recarregar a página)
                this.updateURL();
                
                // Tracking GTM
                this.trackLoadMore();
                
                // Scroll suave para os novos posts
                this.scrollToNewPosts();
                
            } else {
                this.showError('Erro ao carregar mais posts: ' + data.error);
            }
            
        } catch (error) {
            console.error('Erro ao carregar mais posts:', error);
            this.showError('Erro de conexão. Tente novamente.');
        } finally {
            this.isLoading = false;
            this.updateLoadMoreButton(false);
        }
    }
    
    async searchPosts() {
        const query = this.searchInput.value.trim();
        
        if (!query) {
            this.showError('Digite um termo para buscar');
            return;
        }
        
        this.isLoading = true;
        this.updateLoadMoreButton(true, 'Buscando...');
        
        try {
            const params = new URLSearchParams({
                q: query
            });
            
            if (this.currentCategory) {
                params.append('category', this.currentCategory);
            }
            
            const response = await fetch(`/aprenda-marketing-digital/api/search/?${params}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.replacePosts(data.html);
                this.currentPage = 1;
                this.hasMore = data.has_next;
                this.totalPosts = data.total_posts;
                this.currentSearch = query;
                
                // Atualizar URL para SEO
                this.updateURL();
                
                // Tracking GTM
                this.trackSearch(query);
                
            } else {
                this.showError('Erro na busca: ' + data.error);
            }
            
        } catch (error) {
            console.error('Erro na busca:', error);
            this.showError('Erro de conexão. Tente novamente.');
        } finally {
            this.isLoading = false;
            this.updateLoadMoreButton(false);
        }
    }
    
    async filterByCategory() {
        const category = this.categoryFilter.value;
        
        this.isLoading = true;
        this.updateLoadMoreButton(true, 'Filtrando...');
        
        try {
            const params = new URLSearchParams({
                page: 1
            });
            
            if (category) {
                params.append('category', category);
            }
            
            if (this.currentSearch) {
                params.append('search', this.currentSearch);
            }
            
            const response = await fetch(`/aprenda-marketing-digital/api/load-more/?${params}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.replacePosts(data.html);
                this.currentPage = 1;
                this.hasMore = data.has_next;
                this.totalPosts = data.total_posts;
                this.currentCategory = category;
                
                // Atualizar URL para SEO
                this.updateURL();
                
                // Tracking GTM
                this.trackCategoryFilter(category);
                
            } else {
                this.showError('Erro ao filtrar: ' + data.error);
            }
            
        } catch (error) {
            console.error('Erro ao filtrar:', error);
            this.showError('Erro de conexão. Tente novamente.');
        } finally {
            this.isLoading = false;
            this.updateLoadMoreButton(false);
        }
    }
    
    appendPosts(html) {
        // Criar elemento temporário para inserir o HTML
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        
        // Adicionar classe de animação aos novos posts
        const newPosts = tempDiv.querySelectorAll('.blog-card');
        newPosts.forEach((post, index) => {
            post.style.opacity = '0';
            post.style.transform = 'translateY(20px)';
            post.style.transition = 'all 0.5s ease';
            
            // Adicionar ao container
            this.postsContainer.appendChild(post);
            
            // Animar entrada
            setTimeout(() => {
                post.style.opacity = '1';
                post.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }
    
    replacePosts(html) {
        // Limpar posts existentes
        this.postsContainer.innerHTML = '';
        
        // Adicionar novos posts
        this.appendPosts(html);
    }
    
    updateLoadMoreButton(loading, text = null) {
        if (!this.loadMoreBtn) return;
        
        if (loading) {
            this.loadMoreBtn.disabled = true;
            this.loadMoreBtn.innerHTML = text || '<i class="fas fa-spinner fa-spin me-2"></i>Carregando...';
        } else {
            this.loadMoreBtn.disabled = false;
            if (this.hasMore) {
                this.loadMoreBtn.innerHTML = 'Carregar mais';
            } else {
                this.loadMoreBtn.innerHTML = 'Todos os posts carregados';
                this.loadMoreBtn.style.opacity = '0.6';
            }
        }
    }
    
    updateURL() {
        const url = new URL(window.location);
        
        // Atualizar parâmetros da URL
        if (this.currentPage > 1) {
            url.searchParams.set('page', this.currentPage);
        } else {
            url.searchParams.delete('page');
        }
        
        if (this.currentCategory) {
            url.searchParams.set('category', this.currentCategory);
        } else {
            url.searchParams.delete('category');
        }
        
        if (this.currentSearch) {
            url.searchParams.set('search', this.currentSearch);
        } else {
            url.searchParams.delete('search');
        }
        
        // Atualizar URL sem recarregar a página
        window.history.pushState({}, '', url);
        
        // Atualizar título da página para SEO
        this.updatePageTitle();
    }
    
    updatePageTitle() {
        let title = 'Aprenda Marketing Digital - Agência Kaizen';
        
        if (this.currentSearch) {
            title = `Busca: ${this.currentSearch} - ${title}`;
        } else if (this.currentCategory) {
            title = `${this.currentCategory} - ${title}`;
        }
        
        if (this.currentPage > 1) {
            title = `Página ${this.currentPage} - ${title}`;
        }
        
        document.title = title;
    }
    
    scrollToNewPosts() {
        // Scroll suave para os novos posts
        const newPosts = this.postsContainer.querySelectorAll('.blog-card');
        if (newPosts.length > 0) {
            const lastPost = newPosts[newPosts.length - 1];
            lastPost.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }
    }
    
    showError(message) {
        // Criar ou atualizar elemento de erro
        let errorDiv = document.querySelector('.blog-error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'blog-error-message alert alert-danger mt-3';
            errorDiv.style.display = 'none';
            this.postsContainer.parentNode.insertBefore(errorDiv, this.postsContainer);
        }
        
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Esconder erro após 5 segundos
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
    
    // Tracking GTM
    trackLoadMore() {
        if (typeof window.gtmTracking !== 'undefined') {
            window.gtmTracking.trackEvent('blog_load_more', {
                page: this.currentPage,
                category: this.currentCategory,
                search: this.currentSearch,
                total_posts: this.totalPosts
            });
        }
    }
    
    trackSearch(query) {
        if (typeof window.gtmTracking !== 'undefined') {
            window.gtmTracking.trackEvent('blog_search', {
                query: query,
                category: this.currentCategory,
                results_count: this.totalPosts
            });
        }
    }
    
    trackCategoryFilter(category) {
        if (typeof window.gtmTracking !== 'undefined') {
            window.gtmTracking.trackEvent('blog_category_filter', {
                category: category,
                search: this.currentSearch,
                results_count: this.totalPosts
            });
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.blogLoadMore = new BlogLoadMore();
});

