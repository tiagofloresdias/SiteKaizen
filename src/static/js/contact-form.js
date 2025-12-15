/**
 * Validações e máscaras para o formulário de contato
 * Todas as validações em português
 */

class ContactFormValidator {
    constructor() {
        this.form = document.querySelector('form[action="/contato/"]');
        this.init();
    }

    init() {
        if (!this.form) return;

        this.setupMasks();
        this.setupValidations();
        this.setupFormSubmission();
    }

    setupMasks() {
        // Máscara para telefone
        const phoneInput = this.form.querySelector('input[name="phone"]');
        if (phoneInput) {
            phoneInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                
                if (value.length <= 11) {
                    if (value.length <= 2) {
                        value = value;
                    } else if (value.length <= 6) {
                        value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
                    } else if (value.length <= 10) {
                        value = `(${value.slice(0, 2)}) ${value.slice(2, 6)}-${value.slice(6)}`;
                    } else {
                        value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
                    }
                }
                
                e.target.value = value;
            });

            phoneInput.addEventListener('blur', (e) => {
                this.validatePhone(e.target);
            });
        }

        // Máscara e validação para URL
        const websiteInput = this.form.querySelector('input[name="website"]');
        if (websiteInput) {
            websiteInput.addEventListener('blur', (e) => {
                this.formatAndValidateURL(e.target);
            });

            websiteInput.addEventListener('input', (e) => {
                // Remover http:// se o usuário estiver digitando
                if (e.target.value.startsWith('http://') || e.target.value.startsWith('https://')) {
                    // Deixar o usuário digitar normalmente
                }
            });
        }

        // Máscara para nome (apenas letras e espaços)
        const nameInput = this.form.querySelector('input[name="name"]');
        if (nameInput) {
            nameInput.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, '');
            });
        }
    }

    setupValidations() {
        // Validação em tempo real
        const inputs = this.form.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', (e) => {
                this.validateField(e.target);
            });

            input.addEventListener('input', (e) => {
                this.clearFieldError(e.target);
            });
        });
    }

    setupFormSubmission() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            if (this.validateForm()) {
                this.submitForm();
            }
        });
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Limpar erros anteriores
        this.clearFieldError(field);

        // Validações específicas por campo
        switch (field.name) {
            case 'name':
                if (!value) {
                    errorMessage = 'Nome é obrigatório';
                    isValid = false;
                } else if (value.length < 2) {
                    errorMessage = 'Nome deve ter pelo menos 2 caracteres';
                    isValid = false;
                } else if (!/^[a-zA-ZÀ-ÿ\s]+$/.test(value)) {
                    errorMessage = 'Nome deve conter apenas letras';
                    isValid = false;
                }
                break;

            case 'email':
                if (!value) {
                    errorMessage = 'E-mail é obrigatório';
                    isValid = false;
                } else if (!this.isValidEmail(value)) {
                    errorMessage = 'E-mail inválido';
                    isValid = false;
                }
                break;

            case 'phone':
                if (!value) {
                    errorMessage = 'WhatsApp é obrigatório';
                    isValid = false;
                } else if (!this.isValidPhone(value)) {
                    errorMessage = 'WhatsApp inválido. Use o formato (XX) XXXXX-XXXX';
                    isValid = false;
                }
                break;

            case 'message':
                if (!value) {
                    errorMessage = 'Mensagem é obrigatória';
                    isValid = false;
                } else if (value.length < 10) {
                    errorMessage = 'Mensagem deve ter pelo menos 10 caracteres';
                    isValid = false;
                }
                break;

            case 'faturamento':
                if (!value) {
                    errorMessage = 'Faturamento é obrigatório';
                    isValid = false;
                }
                break;

            case 'area':
                if (!value) {
                    errorMessage = 'Área é obrigatória';
                    isValid = false;
                }
                break;

            case 'website':
                if (value && !this.isValidURL(value)) {
                    errorMessage = 'URL inválida';
                    isValid = false;
                }
                break;
        }

        if (!isValid) {
            this.showFieldError(field, errorMessage);
        }

        return isValid;
    }

    validatePhone(phoneInput) {
        const value = phoneInput.value.replace(/\D/g, '');
        return value.length >= 10 && value.length <= 11;
    }

    isValidPhone(phone) {
        const cleanPhone = phone.replace(/\D/g, '');
        return cleanPhone.length >= 10 && cleanPhone.length <= 11;
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    isValidURL(url) {
        try {
            // Adicionar http:// se não tiver protocolo
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                url = 'http://' + url;
            }
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    formatAndValidateURL(urlInput) {
        let value = urlInput.value.trim();
        
        if (value && !value.startsWith('http://') && !value.startsWith('https://')) {
            value = 'http://' + value;
            urlInput.value = value;
        }
    }

    validateForm() {
        const inputs = this.form.querySelectorAll('input[required], select[required], textarea[required]');
        let isFormValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isFormValid = false;
            }
        });

        return isFormValid;
    }

    showFieldError(field, message) {
        // Remover erro anterior se existir
        this.clearFieldError(field);

        // Adicionar classe de erro
        field.classList.add('is-invalid');

        // Criar elemento de erro
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.style.color = '#ffc107';
        errorDiv.style.fontSize = '0.875rem';
        errorDiv.style.marginTop = '0.25rem';

        // Inserir após o campo
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    async submitForm() {
        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // Mostrar loading
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';

        try {
            const formData = new FormData(this.form);
            
            const response = await fetch('/contato/ajax/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                // Sucesso
                this.showSuccessMessage(data.message);
                this.form.reset();
                
                // Tracking GTM
                if (window.gtmTracking) {
                    window.gtmTracking.trackEvent('contact_form_submit', {
                        form_type: 'contact_page',
                        success: true
                    });
                }
            } else {
                // Erro
                this.showErrorMessage(data.message);
                
                // Tracking GTM
                if (window.gtmTracking) {
                    window.gtmTracking.trackEvent('contact_form_error', {
                        form_type: 'contact_page',
                        error: data.message
                    });
                }
            }

        } catch (error) {
            console.error('Erro ao enviar formulário:', error);
            this.showErrorMessage('Erro interno. Tente novamente em alguns instantes.');
            
            // Tracking GTM
            if (window.gtmTracking) {
                window.gtmTracking.trackEvent('contact_form_error', {
                    form_type: 'contact_page',
                    error: 'network_error'
                });
            }
        } finally {
            // Restaurar botão
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    }

    showSuccessMessage(message) {
        if (window.showSuccess) {
            window.showSuccess(message);
        } else {
            alert(message);
        }
    }

    showErrorMessage(message) {
        if (window.showError) {
            window.showError(message);
        } else {
            alert(message);
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new ContactFormValidator();
});

