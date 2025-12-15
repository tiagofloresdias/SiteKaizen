/**
 * Sistema de Tracking Avançado para GTM
 * Captura dados de conversão e envia para Google Tag Manager
 */

class GTMTracking {
    constructor() {
        this.dataLayer = window.dataLayer || [];
        this.init();
    }

    init() {
        // Inicializar dataLayer se não existir
        if (!window.dataLayer) {
            window.dataLayer = [];
        }
    }

    /**
     * Envia evento para GTM
     * @param {string} event - Nome do evento
     * @param {Object} data - Dados do evento
     */
    pushEvent(event, data = {}) {
        this.dataLayer.push({
            event: event,
            ...data,
            timestamp: new Date().toISOString(),
            page_url: window.location.href,
            page_title: document.title
        });
    }

    /**
     * Tracking de conversão de lead
     * @param {Object} leadData - Dados do lead
     */
    trackLeadConversion(leadData) {
        const eventData = {
            event: 'lead_conversion',
            lead_name: leadData.name || '',
            lead_email: leadData.email || '',
            lead_phone: leadData.phone || '',
            lead_company: leadData.company || '',
            lead_revenue: leadData.monthly_revenue || '',
            lead_business_area: leadData.business_area || '',
            lead_challenge: leadData.main_challenge || '',
            lead_website: leadData.website_social || '',
            conversion_value: this.calculateLeadValue(leadData),
            conversion_currency: 'BRL',
            lead_source: leadData.utm_source || 'direct',
            lead_medium: leadData.utm_medium || 'none',
            lead_campaign: leadData.utm_campaign || 'none',
            lead_term: leadData.utm_term || '',
            lead_content: leadData.utm_content || '',
            page_location: window.location.href,
            page_referrer: document.referrer || '',
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('lead_conversion', eventData);
        
        // Evento de compra para GA4 Enhanced Ecommerce
        this.pushEvent('purchase', {
            transaction_id: this.generateTransactionId(leadData.email),
            value: eventData.conversion_value,
            currency: eventData.conversion_currency,
            items: [{
                item_id: 'lead_generation',
                item_name: 'Lead Generation Service',
                category: 'Marketing Services',
                quantity: 1,
                price: eventData.conversion_value
            }],
            lead_name: eventData.lead_name,
            lead_email: eventData.lead_email,
            lead_phone: eventData.lead_phone
        });
        
        // Evento específico para Google Ads
        this.pushEvent('conversion', {
            send_to: 'AW-CONVERSION_ID/CONVERSION_LABEL',
            value: eventData.conversion_value,
            currency: eventData.conversion_currency,
            transaction_id: this.generateTransactionId(leadData.email)
        });

        // Evento para Facebook Pixel
        this.pushEvent('Lead', {
            content_name: 'Lead Form Submission',
            content_category: 'Lead Generation',
            value: eventData.conversion_value,
            currency: eventData.conversion_currency
        });
    }

    /**
     * Tracking de newsletter signup
     * @param {Object} newsletterData - Dados do newsletter
     */
    trackNewsletterSignup(newsletterData) {
        const eventData = {
            event: 'newsletter_signup',
            email: newsletterData.email || '',
            name: newsletterData.name || '',
            source: newsletterData.source || 'unknown',
            utm_source: newsletterData.utm_source || '',
            utm_medium: newsletterData.utm_medium || '',
            utm_campaign: newsletterData.utm_campaign || '',
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('newsletter_signup', eventData);
    }

    /**
     * Tracking de step do funil
     * @param {number} step - Número do step
     * @param {string} action - Ação realizada
     * @param {Object} data - Dados adicionais
     */
    trackFunnelStep(step, action, data = {}) {
        const eventData = {
            event: 'funnel_step',
            step_number: step,
            step_action: action,
            lead_id: data.lead_id || null,
            form_data: data.form_data || {},
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('funnel_step', eventData);
    }

    /**
     * Tracking de agendamento Calendly
     * @param {Object} calendlyData - Dados do Calendly
     */
    trackCalendlyScheduled(calendlyData) {
        const eventData = {
            event: 'calendly_scheduled',
            event_id: calendlyData.event_id || '',
            event_uri: calendlyData.event_uri || '',
            scheduled_date: calendlyData.scheduled_date || '',
            lead_id: calendlyData.lead_id || null,
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('calendly_scheduled', eventData);
    }

    /**
     * Tracking de visualização de página
     * @param {Object} pageData - Dados da página
     */
    trackPageView(pageData = {}) {
        const eventData = {
            event: 'page_view',
            page_title: document.title,
            page_location: window.location.href,
            page_referrer: document.referrer || '',
            utm_source: this.getUrlParameter('utm_source'),
            utm_medium: this.getUrlParameter('utm_medium'),
            utm_campaign: this.getUrlParameter('utm_campaign'),
            utm_term: this.getUrlParameter('utm_term'),
            utm_content: this.getUrlParameter('utm_content'),
            ...pageData
        };

        this.pushEvent('page_view', eventData);
    }

    /**
     * Tracking de clique em CTA
     * @param {string} ctaName - Nome do CTA
     * @param {string} ctaLocation - Localização do CTA
     * @param {Object} additionalData - Dados adicionais
     */
    trackCTAClick(ctaName, ctaLocation, additionalData = {}) {
        const eventData = {
            event: 'cta_click',
            cta_name: ctaName,
            cta_location: ctaLocation,
            page_location: window.location.href,
            ...additionalData
        };

        this.pushEvent('cta_click', eventData);
    }

    /**
     * Calcula valor do lead baseado nos dados
     * @param {Object} leadData - Dados do lead
     * @returns {number} Valor estimado
     */
    calculateLeadValue(leadData) {
        let baseValue = 100; // Valor base

        // Ajustar baseado no faturamento
        const revenueMultipliers = {
            'ate_10k': 1.0,
            '10k_50k': 1.5,
            '50k_100k': 2.0,
            '100k_500k': 3.0,
            '500k_1m': 4.0,
            'acima_1m': 5.0
        };

        if (leadData.monthly_revenue && revenueMultipliers[leadData.monthly_revenue]) {
            baseValue *= revenueMultipliers[leadData.monthly_revenue];
        }

        // Ajustar baseado na área do negócio
        const businessMultipliers = {
            'ecommerce': 1.2,
            'saas': 1.5,
            'servicos': 1.0,
            'varejo': 1.1,
            'industria': 1.3,
            'saude': 1.4,
            'educacao': 1.1,
            'imobiliaria': 1.2,
            'automotivo': 1.1
        };

        if (leadData.business_area && businessMultipliers[leadData.business_area]) {
            baseValue *= businessMultipliers[leadData.business_area];
        }

        return Math.round(baseValue);
    }

    /**
     * Gera ID de transação único
     * @param {string} email - Email do lead
     * @returns {string} ID da transação
     */
    generateTransactionId(email) {
        const timestamp = Date.now();
        const emailHash = this.hashString(email);
        return `lead_${timestamp}_${emailHash}`;
    }

    /**
     * Hash simples para string
     * @param {string} str - String para hashear
     * @returns {string} Hash
     */
    hashString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        return Math.abs(hash).toString(36);
    }

    /**
     * Tracking de envio de formulário
     * @param {string} formName - Nome do formulário
     * @param {string} formLocation - Localização do formulário
     * @param {Object} formData - Dados do formulário
     */
    trackFormSubmit(formName, formLocation, formData = {}) {
        const eventData = {
            event: 'form_submit',
            form_name: formName,
            form_location: formLocation,
            form_data: JSON.stringify(formData),
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('form_submit', eventData);
    }

    /**
     * Tracking de abertura de modal
     * @param {string} modalName - Nome da modal
     * @param {string} modalTrigger - Trigger que abriu a modal
     */
    trackModalOpen(modalName, modalTrigger) {
        const eventData = {
            event: 'modal_open',
            modal_name: modalName,
            modal_trigger: modalTrigger,
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('modal_open', eventData);
    }

    /**
     * Tracking de fechamento de modal
     * @param {string} modalName - Nome da modal
     * @param {string} closeReason - Motivo do fechamento
     */
    trackModalClose(modalName, closeReason) {
        const eventData = {
            event: 'modal_close',
            modal_name: modalName,
            close_reason: closeReason,
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('modal_close', eventData);
    }

    /**
     * Tracking de scroll depth
     * @param {number} depth - Profundidade do scroll (0-100)
     */
    trackScrollDepth(depth) {
        const eventData = {
            event: 'scroll_depth',
            scroll_depth: depth,
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('scroll_depth', eventData);
    }

    /**
     * Tracking de tempo na página
     * @param {number} timeOnPage - Tempo em segundos
     */
    trackTimeOnPage(timeOnPage) {
        const eventData = {
            event: 'time_on_page',
            time_on_page: timeOnPage,
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('time_on_page', eventData);
    }

    /**
     * Tracking de download de arquivo
     * @param {string} fileName - Nome do arquivo
     * @param {string} fileType - Tipo do arquivo
     * @param {string} fileLocation - Localização do arquivo
     */
    trackFileDownload(fileName, fileType, fileLocation) {
        const eventData = {
            event: 'file_download',
            file_name: fileName,
            file_type: fileType,
            file_location: fileLocation,
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('file_download', eventData);
    }

    /**
     * Tracking de clique em link externo
     * @param {string} linkUrl - URL do link
     * @param {string} linkText - Texto do link
     * @param {string} linkLocation - Localização do link
     */
    trackExternalLinkClick(linkUrl, linkText, linkLocation) {
        const eventData = {
            event: 'external_link_click',
            link_url: linkUrl,
            link_text: linkText,
            link_location: linkLocation,
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('external_link_click', eventData);
    }

    /**
     * Tracking de erro de formulário
     * @param {string} formName - Nome do formulário
     * @param {string} errorType - Tipo do erro
     * @param {string} errorMessage - Mensagem do erro
     */
    trackFormError(formName, errorType, errorMessage) {
        const eventData = {
            event: 'form_error',
            form_name: formName,
            error_type: errorType,
            error_message: errorMessage,
            page_location: window.location.href,
            timestamp: new Date().toISOString()
        };

        this.pushEvent('form_error', eventData);
    }

    /**
     * Obtém parâmetro da URL
     * @param {string} name - Nome do parâmetro
     * @returns {string} Valor do parâmetro
     */
    getUrlParameter(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name) || '';
    }

    /**
     * Captura UTM parameters da URL
     * @returns {Object} Parâmetros UTM
     */
    getUTMParameters() {
        return {
            utm_source: this.getUrlParameter('utm_source'),
            utm_medium: this.getUrlParameter('utm_medium'),
            utm_campaign: this.getUrlParameter('utm_campaign'),
            utm_term: this.getUrlParameter('utm_term'),
            utm_content: this.getUrlParameter('utm_content')
        };
    }
}

// Instância global
window.gtmTracking = new GTMTracking();

// Auto-tracking de página
document.addEventListener('DOMContentLoaded', function() {
    window.gtmTracking.trackPageView();
});

// Métodos globais para compatibilidade
window.trackLeadConversion = (data) => window.gtmTracking.trackLeadConversion(data);
window.trackNewsletterSignup = (data) => window.gtmTracking.trackNewsletterSignup(data);
window.trackFunnelStep = (step, action, data) => window.gtmTracking.trackFunnelStep(step, action, data);
window.trackCalendlyScheduled = (data) => window.gtmTracking.trackCalendlyScheduled(data);
window.trackCTAClick = (name, location, data) => window.gtmTracking.trackCTAClick(name, location, data);
window.trackFormSubmit = (formName, formLocation, formData) => window.gtmTracking.trackFormSubmit(formName, formLocation, formData);
window.trackModalOpen = (modalName, modalTrigger) => window.gtmTracking.trackModalOpen(modalName, modalTrigger);
window.trackModalClose = (modalName, closeReason) => window.gtmTracking.trackModalClose(modalName, closeReason);
window.trackScrollDepth = (depth) => window.gtmTracking.trackScrollDepth(depth);
window.trackTimeOnPage = (timeOnPage) => window.gtmTracking.trackTimeOnPage(timeOnPage);
window.trackFileDownload = (fileName, fileType, fileLocation) => window.gtmTracking.trackFileDownload(fileName, fileType, fileLocation);
window.trackExternalLinkClick = (linkUrl, linkText, linkLocation) => window.gtmTracking.trackExternalLinkClick(linkUrl, linkText, linkLocation);
window.trackFormError = (formName, errorType, errorMessage) => window.gtmTracking.trackFormError(formName, errorType, errorMessage);
