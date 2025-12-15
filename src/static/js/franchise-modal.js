/**
 * Sistema de Modal de Franqueado
 * Controla o fluxo de 6 passos para aplicação de franqueado
 */

class FranchiseModal {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 6;
        this.applicationId = null;
        this.formData = {};
        this.modal = null;
        
        this.init();
    }
    
    init() {
        // Aguardar carregamento do DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
    }
    
    setupEventListeners() {
        // Botão para abrir modal
        const franchiseButtons = document.querySelectorAll('[data-franchise-modal]');
        franchiseButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.openModal();
            });
        });
        
        // Botões de navegação
        const nextBtn = document.getElementById('franchise-next-btn');
        const prevBtn = document.getElementById('franchise-prev-btn');
        const submitBtn = document.getElementById('franchise-submit-btn');
        
        if (nextBtn) nextBtn.addEventListener('click', () => this.nextStep());
        if (prevBtn) prevBtn.addEventListener('click', () => this.prevStep());
        if (submitBtn) submitBtn.addEventListener('click', () => this.submitApplication());
        
        // Botão de download do kit
        const downloadKitBtn = document.getElementById('franchise-download-kit');
        if (downloadKitBtn) {
            downloadKitBtn.addEventListener('click', () => this.downloadKit());
        }
        
        // Máscaras de input
        this.setupInputMasks();
        
        // Validação em tempo real
        this.setupValidation();
    }
    
    setupInputMasks() {
        // Máscara para telefone
        const phoneInput = document.getElementById('franchise-phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 11) {
                    value = value.replace(/(\d{2})(\d{4,5})(\d{4})/, '($1) $2-$3');
                    e.target.value = value;
                }
            });
        }
        
        // Máscara para CPF
        const cpfInput = document.getElementById('franchise-cpf');
        if (cpfInput) {
            cpfInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 11) {
                    value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
                    e.target.value = value;
                }
            });
        }
        
        // Máscara para RG
        const rgInput = document.getElementById('franchise-rg');
        if (rgInput) {
            rgInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 9) {
                    value = value.replace(/(\d{2})(\d{3})(\d{3})(\d{1})/, '$1.$2.$3-$4');
                    e.target.value = value;
                }
            });
        }
        
        // Máscara para CEP
        const zipcodeInput = document.getElementById('franchise-zipcode');
        if (zipcodeInput) {
            zipcodeInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 8) {
                    value = value.replace(/(\d{5})(\d{3})/, '$1-$2');
                    e.target.value = value;
                }
            });
        }
    }
    
    setupValidation() {
        // Validação em tempo real para campos obrigatórios
        const requiredFields = document.querySelectorAll('#franchiseModal [required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', () => this.validateField(field));
            field.addEventListener('input', () => this.clearFieldError(field));
        });
    }
    
    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let errorMessage = '';
        
        // Validações específicas
        if (fieldName === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (value && !emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'E-mail inválido';
            }
        } else if (fieldName === 'phone') {
            const phoneRegex = /^\(\d{2}\)\s\d{4,5}-\d{4}$/;
            if (value && !phoneRegex.test(value)) {
                isValid = false;
                errorMessage = 'Telefone inválido. Use o formato (11) 99999-9999';
            }
        } else if (fieldName === 'cpf') {
            if (value && !this.validateCPF(value)) {
                isValid = false;
                errorMessage = 'CPF inválido';
            }
        } else if (fieldName === 'zipcode') {
            const zipcodeRegex = /^\d{5}-\d{3}$/;
            if (value && !zipcodeRegex.test(value)) {
                isValid = false;
                errorMessage = 'CEP inválido. Use o formato 00000-000';
            }
        } else if (field.required && !value) {
            isValid = false;
            errorMessage = 'Este campo é obrigatório';
        }
        
        if (!isValid) {
            this.showFieldError(field, errorMessage);
        } else {
            this.clearFieldError(field);
        }
        
        return isValid;
    }
    
    validateCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        
        if (cpf.length !== 11) return false;
        if (cpf === cpf[0].repeat(11)) return false;
        
        // Validação do primeiro dígito
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf[i]) * (10 - i);
        }
        let digit1 = 11 - (sum % 11);
        if (digit1 >= 10) digit1 = 0;
        
        if (parseInt(cpf[9]) !== digit1) return false;
        
        // Validação do segundo dígito
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf[i]) * (11 - i);
        }
        let digit2 = 11 - (sum % 11);
        if (digit2 >= 10) digit2 = 0;
        
        return parseInt(cpf[10]) === digit2;
    }
    
    showFieldError(field, message) {
        this.clearFieldError(field);
        
        field.classList.add('is-invalid');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
    }
    
    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    openModal() {
        // Tracking
        if (window.gtmTracking) {
            window.gtmTracking.trackModalOpen('franchise_modal', 'button_click');
        }
        
        // Reset do modal
        this.currentStep = 1;
        this.applicationId = null;
        this.formData = {};
        
        // Mostrar modal
        this.modal = new bootstrap.Modal(document.getElementById('franchiseModal'));
        this.modal.show();
        
        // Atualizar display
        this.updateStepDisplay();
        
        // Tracking do início do processo
        this.trackStep(1, 'start');
    }
    
    closeModal() {
        if (this.modal) {
            this.modal.hide();
        }
        
        // Tracking
        if (window.gtmTracking) {
            window.gtmTracking.trackModalClose('franchise_modal', 'user_close');
        }
    }
    
    nextStep() {
        if (this.validateCurrentStep()) {
            this.saveCurrentStep().then(() => {
                if (this.currentStep < this.totalSteps) {
                    this.currentStep++;
                    this.updateStepDisplay();
                    this.trackStep(this.currentStep, 'start');
                }
            }).catch(error => {
                console.error('Erro ao salvar step:', error);
                this.showError('Erro ao salvar dados', error.message);
            });
        }
    }
    
    prevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateStepDisplay();
        }
    }
    
    updateStepDisplay() {
        // Atualizar progress bar
        const progress = document.getElementById('franchise-progress');
        if (progress) {
            const percentage = (this.currentStep / this.totalSteps) * 100;
            progress.style.width = percentage + '%';
        }
        
        // Atualizar step indicator
        const steps = document.querySelectorAll('.step-indicator .step');
        steps.forEach((step, index) => {
            step.classList.remove('active', 'completed');
            if (index + 1 < this.currentStep) {
                step.classList.add('completed');
            } else if (index + 1 === this.currentStep) {
                step.classList.add('active');
            }
        });
        
        // Mostrar/ocultar painéis
        const panels = document.querySelectorAll('.step-panel');
        panels.forEach((panel, index) => {
            panel.classList.remove('active');
            if (index + 1 === this.currentStep) {
                panel.classList.add('active');
            }
        });
        
        // Atualizar botões
        const prevBtn = document.getElementById('franchise-prev-btn');
        const nextBtn = document.getElementById('franchise-next-btn');
        const submitBtn = document.getElementById('franchise-submit-btn');
        
        if (prevBtn) {
            prevBtn.style.display = this.currentStep > 1 ? 'inline-block' : 'none';
        }
        
        if (nextBtn) {
            nextBtn.style.display = this.currentStep < this.totalSteps ? 'inline-block' : 'none';
        }
        
        if (submitBtn) {
            submitBtn.style.display = this.currentStep === this.totalSteps ? 'inline-block' : 'none';
        }
    }
    
    validateCurrentStep() {
        const currentPanel = document.querySelector(`#franchise-step${this.currentStep}`);
        if (!currentPanel) return true;
        
        const requiredFields = currentPanel.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    saveCurrentStep() {
        const form = document.getElementById(`franchise-form-step${this.currentStep}`);
        if (!form) return Promise.resolve();
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Adicionar dados de tracking
        data.utm_source = this.getUTMParameter('utm_source');
        data.utm_medium = this.getUTMParameter('utm_medium');
        data.utm_campaign = this.getUTMParameter('utm_campaign');
        data.utm_term = this.getUTMParameter('utm_term');
        data.utm_content = this.getUTMParameter('utm_content');
        data.referrer = document.referrer;
        data.landing_page = window.location.href;
        data.session_id = this.getSessionId();
        
        if (this.applicationId) {
            data.application_id = this.applicationId;
        }
        
        return fetch(`/franchise/api/step${this.currentStep}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                if (result.application_id) {
                    this.applicationId = result.application_id;
                }
                
                // Notificação de sucesso
                if (window.showSuccess) {
                    window.showSuccess(
                        'i18n.franchise.success.step' + this.currentStep,
                        '',
                        { duration: 2000 }
                    );
                }
                
                return result;
            } else {
                throw new Error(result.error || 'Erro ao salvar dados');
            }
        });
    }
    
    submitApplication() {
        if (!this.validateCurrentStep()) return;
        
        this.saveCurrentStep().then(() => {
            // Enviar aplicação final
            return fetch('/franchise/api/submit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    application_id: this.applicationId
                })
            });
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                // Tracking de conversão
                if (window.gtmTracking) {
                    window.gtmTracking.trackLeadConversion({
                        name: this.formData.full_name || '',
                        email: this.formData.email || '',
                        phone: this.formData.phone || '',
                        company: 'Franchise Application',
                        utm_source: this.getUTMParameter('utm_source'),
                        utm_medium: this.getUTMParameter('utm_medium'),
                        utm_campaign: this.getUTMParameter('utm_campaign'),
                        conversion_type: 'franchise_application'
                    });
                }
                
                // Notificação de sucesso
                if (window.showSuccess) {
                    window.showSuccess(
                        'i18n.franchise.success.complete',
                        'i18n.franchise.success.complete_message',
                        { duration: 5000 }
                    );
                }
                
                // Ir para step final
                this.currentStep = this.totalSteps;
                this.updateStepDisplay();
                
            } else {
                throw new Error(result.error || 'Erro ao enviar aplicação');
            }
        })
        .catch(error => {
            console.error('Erro ao enviar aplicação:', error);
            this.showError('Erro ao enviar aplicação', error.message);
        });
    }
    
    trackStep(step, action) {
        if (this.applicationId && window.gtmTracking) {
            window.gtmTracking.trackFunnelStep(step, action, {
                application_id: this.applicationId,
                step_name: `franchise_step_${step}`
            });
        }
    }
    
    downloadKit() {
        // Simular download do kit
        const link = document.createElement('a');
        link.href = '/static/documents/kit-franqueado-kaizen.pdf';
        link.download = 'kit-franqueado-kaizen.pdf';
        link.click();
        
        // Tracking
        if (window.gtmTracking) {
            window.gtmTracking.trackFileDownload('kit-franqueado-kaizen.pdf', 'pdf', 'franchise_modal');
        }
    }
    
    showError(title, message) {
        if (window.showError) {
            window.showError(title, message);
        } else {
            alert(`${title}: ${message}`);
        }
    }
    
    getUTMParameter(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name) || '';
    }
    
    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }
    
    getSessionId() {
        // Gerar ou recuperar session ID
        let sessionId = sessionStorage.getItem('franchise_session_id');
        if (!sessionId) {
            sessionId = 'franchise_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('franchise_session_id', sessionId);
        }
        return sessionId;
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.franchiseModal = new FranchiseModal();
});

// Exportar para uso global
window.FranchiseModal = FranchiseModal;

