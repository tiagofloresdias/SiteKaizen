/**
 * Sistema de Notificações Suaves
 * Sistema moderno de notificações para formulários e interações
 */

class NotificationSystem {
    constructor() {
        this.container = null;
        this.notifications = new Map();
        this.init();
    }

    init() {
        // Criar container se não existir
        if (!document.getElementById('notification-container')) {
            this.createContainer();
        }
        this.container = document.getElementById('notification-container');
    }

    createContainer() {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'notification-container';
        document.body.appendChild(container);
    }

    /**
     * Mostra uma notificação
     * @param {Object} options - Opções da notificação
     * @param {string} options.type - Tipo: success, error, warning, info
     * @param {string} options.title - Título da notificação
     * @param {string} options.message - Mensagem da notificação
     * @param {number} options.duration - Duração em ms (padrão: 5000)
     * @param {boolean} options.autoClose - Fechar automaticamente (padrão: true)
     * @param {Function} options.onClose - Callback ao fechar
     * @param {Object} options.params - Parâmetros para tradução
     */
    show({
        type = 'info',
        title = '',
        message = '',
        duration = 5000,
        autoClose = true,
        onClose = null,
        params = {}
    } = {}) {
        const id = this.generateId();
        
        // Traduzir título e mensagem se necessário
        const translatedTitle = title.startsWith('i18n.') ? this.translate(title, params) : title;
        const translatedMessage = message.startsWith('i18n.') ? this.translate(message, params) : message;
        
        const notification = this.createNotification({
            id,
            type,
            title: translatedTitle,
            message: translatedMessage,
            duration,
            autoClose,
            onClose
        });

        this.container.appendChild(notification);
        this.notifications.set(id, notification);

        // Animar entrada
        setTimeout(() => {
            notification.classList.add('show', 'notification-enter');
        }, 10);

        // Auto close
        if (autoClose && duration > 0) {
            setTimeout(() => {
                this.hide(id);
            }, duration);
        }

        return id;
    }

    createNotification({ id, type, title, message, duration, autoClose, onClose }) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.dataset.id = id;

        const icon = this.getIcon(type);
        
        notification.innerHTML = `
            <div class="notification-header">
                <div class="notification-icon">${icon}</div>
                <h6 class="notification-title">${title}</h6>
                <button class="notification-close" onclick="notificationSystem.hide('${id}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <p class="notification-message">${message}</p>
            ${autoClose && duration > 0 ? '<div class="notification-progress"></div>' : ''}
        `;

        // Callback de fechamento
        if (onClose) {
            notification.dataset.onClose = 'true';
            notification.addEventListener('close', onClose);
        }

        return notification;
    }

    getIcon(type) {
        const icons = {
            success: '<i class="fas fa-check"></i>',
            error: '<i class="fas fa-exclamation"></i>',
            warning: '<i class="fas fa-exclamation-triangle"></i>',
            info: '<i class="fas fa-info"></i>'
        };
        return icons[type] || icons.info;
    }

    /**
     * Esconde uma notificação
     * @param {string} id - ID da notificação
     */
    hide(id) {
        const notification = this.notifications.get(id);
        if (!notification) return;

        notification.classList.add('notification-exit');
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            this.notifications.delete(id);
        }, 300);
    }

    /**
     * Esconde todas as notificações
     */
    hideAll() {
        this.notifications.forEach((notification, id) => {
            this.hide(id);
        });
    }

    generateId() {
        return 'notification_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Traduz uma chave usando o sistema i18n
     * @param {string} key - Chave da tradução (com ou sem prefixo i18n.)
     * @param {Object} params - Parâmetros para substituição
     * @returns {string} Texto traduzido
     */
    translate(key, params = {}) {
        // Remover prefixo i18n. se presente
        const cleanKey = key.startsWith('i18n.') ? key.substring(5) : key;
        
        // Usar sistema i18n se disponível
        if (window.i18n) {
            return window.i18n.t(cleanKey, params);
        }
        
        // Fallback para a chave original
        return key;
    }

    // Métodos de conveniência
    success(title, message, options = {}) {
        return this.show({ type: 'success', title, message, ...options });
    }

    error(title, message, options = {}) {
        return this.show({ type: 'error', title, message, duration: 0, autoClose: false, ...options });
    }

    warning(title, message, options = {}) {
        return this.show({ type: 'warning', title, message, ...options });
    }

    info(title, message, options = {}) {
        return this.show({ type: 'info', title, message, ...options });
    }
}

// Instância global
window.notificationSystem = new NotificationSystem();

// Métodos globais para compatibilidade
window.showNotification = (options) => window.notificationSystem.show(options);
window.showSuccess = (title, message, options) => window.notificationSystem.success(title, message, options);
window.showError = (title, message, options) => window.notificationSystem.error(title, message, options);
window.showWarning = (title, message, options) => window.notificationSystem.warning(title, message, options);
window.showInfo = (title, message, options) => window.notificationSystem.info(title, message, options);

// Auto-inicialização quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.notificationSystem.init();
    });
} else {
    window.notificationSystem.init();
}
