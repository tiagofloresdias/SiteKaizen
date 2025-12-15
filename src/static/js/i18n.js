/**
 * Sistema de Internacionalização (i18n) para JavaScript
 * Suporte a múltiplos idiomas com português como padrão
 */

class I18n {
    constructor() {
        this.currentLanguage = this.detectLanguage();
        this.translations = {
            'pt-br': {
                // Validações de formulário
                'validation.required': 'Este campo é obrigatório.',
                'validation.email': 'Por favor, insira um e-mail válido.',
                'validation.phone': 'Por favor, insira um telefone válido no formato (11) 99999-9999.',
                'validation.min_length': 'Este campo deve ter pelo menos {min} caracteres.',
                'validation.max_length': 'Este campo deve ter no máximo {max} caracteres.',
                'validation.numeric': 'Este campo deve conter apenas números.',
                'validation.alpha': 'Este campo deve conter apenas letras.',
                'validation.alpha_numeric': 'Este campo deve conter apenas letras e números.',
                'validation.url': 'Por favor, insira uma URL válida.',
                'validation.date': 'Por favor, insira uma data válida.',
                'validation.time': 'Por favor, insira um horário válido.',
                'validation.credit_card': 'Por favor, insira um número de cartão válido.',
                'validation.cpf': 'Por favor, insira um CPF válido.',
                'validation.cnpj': 'Por favor, insira um CNPJ válido.',
                'validation.cep': 'Por favor, insira um CEP válido.',
                
                // Mensagens de sucesso
                'success.form_saved': 'Dados salvos com sucesso!',
                'success.newsletter_subscribed': 'Inscrição realizada com sucesso!',
                'success.contact_sent': 'Mensagem enviada com sucesso!',
                'success.file_uploaded': 'Arquivo enviado com sucesso!',
                'success.data_updated': 'Dados atualizados com sucesso!',
                
                // Mensagens de erro
                'error.generic': 'Ocorreu um erro inesperado. Tente novamente.',
                'error.network': 'Erro de conexão. Verifique sua internet.',
                'error.server': 'Erro interno do servidor. Tente novamente mais tarde.',
                'error.validation': 'Por favor, corrija os erros no formulário.',
                'error.required_fields': 'Por favor, preencha todos os campos obrigatórios.',
                'error.invalid_data': 'Dados inválidos. Verifique as informações.',
                'error.duplicate_email': 'Este e-mail já está cadastrado.',
                'error.invalid_credentials': 'Credenciais inválidas.',
                'error.session_expired': 'Sua sessão expirou. Faça login novamente.',
                
                // Mensagens de aviso
                'warning.unsaved_changes': 'Você tem alterações não salvas.',
                'warning.confirm_action': 'Tem certeza que deseja realizar esta ação?',
                'warning.data_loss': 'Esta ação pode causar perda de dados.',
                'warning.low_storage': 'Espaço de armazenamento baixo.',
                'warning.maintenance': 'Sistema em manutenção. Tente novamente mais tarde.',
                
                // Mensagens informativas
                'info.loading': 'Carregando...',
                'info.saving': 'Salvando...',
                'info.processing': 'Processando...',
                'info.uploading': 'Enviando arquivo...',
                'info.downloading': 'Baixando arquivo...',
                'info.connecting': 'Conectando...',
                'info.disconnected': 'Desconectado.',
                'info.reconnecting': 'Reconectando...',
                
                // Labels de formulário
                'form.name': 'Nome',
                'form.email': 'E-mail',
                'form.phone': 'Telefone',
                'form.message': 'Mensagem',
                'form.subject': 'Assunto',
                'form.company': 'Empresa',
                'form.website': 'Website',
                'form.address': 'Endereço',
                'form.city': 'Cidade',
                'form.state': 'Estado',
                'form.zipcode': 'CEP',
                'form.country': 'País',
                'form.birth_date': 'Data de Nascimento',
                'form.gender': 'Gênero',
                'form.newsletter': 'Newsletter',
                'form.terms': 'Termos e Condições',
                'form.privacy': 'Política de Privacidade',
                
                // Botões
                'button.save': 'Salvar',
                'button.cancel': 'Cancelar',
                'button.submit': 'Enviar',
                'button.send': 'Enviar',
                'button.close': 'Fechar',
                'button.delete': 'Excluir',
                'button.edit': 'Editar',
                'button.add': 'Adicionar',
                'button.remove': 'Remover',
                'button.confirm': 'Confirmar',
                'button.back': 'Voltar',
                'button.next': 'Próximo',
                'button.previous': 'Anterior',
                'button.finish': 'Finalizar',
                'button.continue': 'Continuar',
                'button.retry': 'Tentar Novamente',
                'button.refresh': 'Atualizar',
                'button.download': 'Baixar',
                'button.upload': 'Enviar',
                'button.search': 'Buscar',
                'button.filter': 'Filtrar',
                'button.clear': 'Limpar',
                'button.reset': 'Resetar',
                'button.load_more': 'Carregar Mais',
                'button.show_more': 'Mostrar Mais',
                'button.show_less': 'Mostrar Menos',
                
                // Placeholders
                'placeholder.name': 'Digite seu nome completo',
                'placeholder.email': 'Digite seu e-mail',
                'placeholder.phone': '(11) 99999-9999',
                'placeholder.message': 'Digite sua mensagem',
                'placeholder.search': 'Digite para buscar...',
                'placeholder.select': 'Selecione uma opção',
                'placeholder.date': 'DD/MM/AAAA',
                'placeholder.time': 'HH:MM',
                'placeholder.url': 'https://exemplo.com',
                'placeholder.password': 'Digite sua senha',
                'placeholder.confirm_password': 'Confirme sua senha',
                
                // Títulos e cabeçalhos
                'title.contact': 'Fale Conosco',
                'title.newsletter': 'Newsletter',
                'title.login': 'Login',
                'title.register': 'Cadastro',
                'title.profile': 'Perfil',
                'title.settings': 'Configurações',
                'title.help': 'Ajuda',
                'title.about': 'Sobre',
                'title.terms': 'Termos de Uso',
                'title.privacy': 'Política de Privacidade',
                'title.cookies': 'Política de Cookies',
                
                // Mensagens específicas do site
                'site.lead_form_title': 'Consulte um dos nossos especialistas sem nenhum custo',
                'site.newsletter_title': 'Receba nossos insights',
                'site.newsletter_subtitle': 'Fique por dentro das melhores estratégias de marketing digital.',
                'site.contact_success': 'Mensagem enviada com sucesso! Nossa equipe entrará em contato em breve.',
                'site.newsletter_success': 'Inscrição realizada com sucesso! Você receberá nossos insights em breve.',
                'site.modal_title': 'Converse com o Especialista',
                'site.step1_title': 'Vamos começar! Conte-nos sobre você',
                'site.step2_title': 'Fale mais sobre seu negócio',
                'site.step3_title': 'Agende sua reunião estratégica',
                'site.step4_title': 'Agendamento Concluído!',
                
                // Fluxo de franqueado
                'franchise.modal_title': 'Torne-se um Franqueado Kaizen',
                'franchise.step1_title': 'Dados Pessoais',
                'franchise.step1_subtitle': 'Conte-nos sobre você para começarmos',
                'franchise.step2_title': 'Perfil Profissional',
                'franchise.step2_subtitle': 'Fale sobre sua experiência e objetivos',
                'franchise.step3_title': 'Investimento e Localização',
                'franchise.step3_subtitle': 'Informações sobre investimento e região de interesse',
                'franchise.step4_title': 'Documentação',
                'franchise.step4_subtitle': 'Envie os documentos necessários',
                'franchise.step5_title': 'Agendamento',
                'franchise.step5_subtitle': 'Agende sua reunião com nosso time de franquias',
                'franchise.step6_title': 'Processo Iniciado!',
                'franchise.step6_subtitle': 'Seu processo de franqueado foi iniciado com sucesso',
                
                // Campos específicos de franqueado
                'form.full_name': 'Nome Completo',
                'form.cpf': 'CPF',
                'form.rg': 'RG',
                'form.birth_date': 'Data de Nascimento',
                'form.marital_status': 'Estado Civil',
                'form.nationality': 'Nacionalidade',
                'form.profession': 'Profissão',
                'form.current_company': 'Empresa Atual',
                'form.current_position': 'Cargo Atual',
                'form.experience_years': 'Anos de Experiência',
                'form.education_level': 'Nível de Escolaridade',
                'form.management_experience': 'Experiência em Gestão',
                'form.sales_experience': 'Experiência em Vendas',
                'form.marketing_experience': 'Experiência em Marketing',
                'form.investment_capacity': 'Capacidade de Investimento',
                'form.preferred_city': 'Cidade de Interesse',
                'form.preferred_state': 'Estado de Interesse',
                'form.preferred_region': 'Região de Interesse',
                'form.expected_start_date': 'Data Esperada para Início',
                'form.team_size': 'Tamanho da Equipe Pretendida',
                'form.target_market': 'Mercado-Alvo de Interesse',
                'form.business_goals': 'Objetivos de Negócio',
                'form.why_franchise': 'Por que quer ser franqueado?',
                'form.expected_revenue': 'Receita Esperada',
                'form.available_time': 'Tempo Disponível para o Negócio',
                'form.risk_tolerance': 'Tolerância ao Risco',
                'form.references': 'Referências',
                'form.documents': 'Documentos',
                'form.curriculum': 'Currículo',
                'form.business_plan': 'Plano de Negócios',
                'form.financial_statement': 'Demonstrativo Financeiro',
                'form.identity_document': 'Documento de Identidade',
                'form.address_proof': 'Comprovante de Endereço',
                'form.income_proof': 'Comprovante de Renda',
                
                // Opções de seleção
                'options.marital_status.single': 'Solteiro(a)',
                'options.marital_status.married': 'Casado(a)',
                'options.marital_status.divorced': 'Divorciado(a)',
                'options.marital_status.widowed': 'Viúvo(a)',
                'options.education_level.elementary': 'Ensino Fundamental',
                'options.education_level.high_school': 'Ensino Médio',
                'options.education_level.technical': 'Técnico',
                'options.education_level.college': 'Superior',
                'options.education_level.postgraduate': 'Pós-graduação',
                'options.education_level.master': 'Mestrado',
                'options.education_level.phd': 'Doutorado',
                'options.experience_level.none': 'Nenhuma',
                'options.experience_level.low': 'Pouca (1-2 anos)',
                'options.experience_level.medium': 'Média (3-5 anos)',
                'options.experience_level.high': 'Alta (6-10 anos)',
                'options.experience_level.expert': 'Expert (10+ anos)',
                'options.investment_capacity.low': 'Até R$ 50.000',
                'options.investment_capacity.medium': 'R$ 50.000 - R$ 150.000',
                'options.investment_capacity.high': 'R$ 150.000 - R$ 300.000',
                'options.investment_capacity.very_high': 'Acima de R$ 300.000',
                'options.team_size.solo': 'Só eu',
                'options.team_size.small': '2-5 pessoas',
                'options.team_size.medium': '6-15 pessoas',
                'options.team_size.large': '16-50 pessoas',
                'options.team_size.enterprise': '50+ pessoas',
                'options.risk_tolerance.low': 'Baixa',
                'options.risk_tolerance.medium': 'Média',
                'options.risk_tolerance.high': 'Alta',
                'options.time_availability.part_time': 'Meio período',
                'options.time_availability.full_time': 'Tempo integral',
                'options.time_availability.weekends': 'Fins de semana',
                'options.time_availability.flexible': 'Flexível',
                
                // Mensagens de sucesso específicas
                'franchise.success.step1': 'Dados pessoais salvos! Vamos para o próximo passo.',
                'franchise.success.step2': 'Perfil profissional registrado! Continue o processo.',
                'franchise.success.step3': 'Informações de investimento salvas! Quase lá.',
                'franchise.success.step4': 'Documentos enviados! Último passo.',
                'franchise.success.step5': 'Agendamento realizado! Aguarde nosso contato.',
                'franchise.success.complete': 'Processo de franqueado iniciado com sucesso!',
                
                // Mensagens de erro específicas
                'franchise.error.invalid_cpf': 'CPF inválido. Verifique o número digitado.',
                'franchise.error.invalid_rg': 'RG inválido. Verifique o número digitado.',
                'franchise.error.invalid_phone': 'Telefone inválido. Use o formato (11) 99999-9999.',
                'franchise.error.invalid_email': 'E-mail inválido. Verifique o endereço digitado.',
                'franchise.error.file_too_large': 'Arquivo muito grande. Máximo 10MB.',
                'franchise.error.invalid_file_type': 'Tipo de arquivo inválido. Use PDF, DOC ou DOCX.',
                'franchise.error.required_documents': 'Documentos obrigatórios não enviados.',
                'franchise.error.invalid_date': 'Data inválida. Use o formato DD/MM/AAAA.',
                
                // Placeholders específicos
                'placeholder.cpf': '000.000.000-00',
                'placeholder.rg': '00.000.000-0',
                'placeholder.phone': '(11) 99999-9999',
                'placeholder.cep': '00000-000',
                'placeholder.investment_amount': 'R$ 0,00',
                'placeholder.expected_revenue': 'R$ 0,00',
                'placeholder.team_size': 'Ex: 5 pessoas',
                'placeholder.business_goals': 'Descreva seus objetivos de negócio...',
                'placeholder.why_franchise': 'Por que você quer ser um franqueado Kaizen?',
                'placeholder.references': 'Nome, telefone e e-mail de 2 referências...',
                
                // Botões específicos
                'button.become_franchisee': 'Quero ser Franqueado',
                'button.start_process': 'Iniciar Processo',
                'button.continue_process': 'Continuar Processo',
                'button.finish_process': 'Finalizar Processo',
                'button.upload_documents': 'Enviar Documentos',
                'button.schedule_meeting': 'Agendar Reunião',
                'button.download_kit': 'Baixar Kit Franqueado',
            },
            'en': {
                // Form validation
                'validation.required': 'This field is required.',
                'validation.email': 'Please enter a valid email address.',
                'validation.phone': 'Please enter a valid phone number.',
                'validation.min_length': 'This field must be at least {min} characters.',
                'validation.max_length': 'This field must be no more than {max} characters.',
                'validation.numeric': 'This field must contain only numbers.',
                'validation.alpha': 'This field must contain only letters.',
                'validation.alpha_numeric': 'This field must contain only letters and numbers.',
                'validation.url': 'Please enter a valid URL.',
                'validation.date': 'Please enter a valid date.',
                'validation.time': 'Please enter a valid time.',
                'validation.credit_card': 'Please enter a valid credit card number.',
                'validation.cpf': 'Please enter a valid CPF.',
                'validation.cnpj': 'Please enter a valid CNPJ.',
                'validation.cep': 'Please enter a valid ZIP code.',
                
                // Success messages
                'success.form_saved': 'Data saved successfully!',
                'success.newsletter_subscribed': 'Subscription successful!',
                'success.contact_sent': 'Message sent successfully!',
                'success.file_uploaded': 'File uploaded successfully!',
                'success.data_updated': 'Data updated successfully!',
                
                // Error messages
                'error.generic': 'An unexpected error occurred. Please try again.',
                'error.network': 'Connection error. Please check your internet.',
                'error.server': 'Internal server error. Please try again later.',
                'error.validation': 'Please correct the errors in the form.',
                'error.required_fields': 'Please fill in all required fields.',
                'error.invalid_data': 'Invalid data. Please check the information.',
                'error.duplicate_email': 'This email is already registered.',
                'error.invalid_credentials': 'Invalid credentials.',
                'error.session_expired': 'Your session has expired. Please log in again.',
                
                // Warning messages
                'warning.unsaved_changes': 'You have unsaved changes.',
                'warning.confirm_action': 'Are you sure you want to perform this action?',
                'warning.data_loss': 'This action may cause data loss.',
                'warning.low_storage': 'Low storage space.',
                'warning.maintenance': 'System under maintenance. Please try again later.',
                
                // Info messages
                'info.loading': 'Loading...',
                'info.saving': 'Saving...',
                'info.processing': 'Processing...',
                'info.uploading': 'Uploading file...',
                'info.downloading': 'Downloading file...',
                'info.connecting': 'Connecting...',
                'info.disconnected': 'Disconnected.',
                'info.reconnecting': 'Reconnecting...',
                
                // Form labels
                'form.name': 'Name',
                'form.email': 'Email',
                'form.phone': 'Phone',
                'form.message': 'Message',
                'form.subject': 'Subject',
                'form.company': 'Company',
                'form.website': 'Website',
                'form.address': 'Address',
                'form.city': 'City',
                'form.state': 'State',
                'form.zipcode': 'ZIP Code',
                'form.country': 'Country',
                'form.birth_date': 'Birth Date',
                'form.gender': 'Gender',
                'form.newsletter': 'Newsletter',
                'form.terms': 'Terms and Conditions',
                'form.privacy': 'Privacy Policy',
                
                // Buttons
                'button.save': 'Save',
                'button.cancel': 'Cancel',
                'button.submit': 'Submit',
                'button.send': 'Send',
                'button.close': 'Close',
                'button.delete': 'Delete',
                'button.edit': 'Edit',
                'button.add': 'Add',
                'button.remove': 'Remove',
                'button.confirm': 'Confirm',
                'button.back': 'Back',
                'button.next': 'Next',
                'button.previous': 'Previous',
                'button.finish': 'Finish',
                'button.continue': 'Continue',
                'button.retry': 'Try Again',
                'button.refresh': 'Refresh',
                'button.download': 'Download',
                'button.upload': 'Upload',
                'button.search': 'Search',
                'button.filter': 'Filter',
                'button.clear': 'Clear',
                'button.reset': 'Reset',
                'button.load_more': 'Load More',
                'button.show_more': 'Show More',
                'button.show_less': 'Show Less',
                
                // Placeholders
                'placeholder.name': 'Enter your full name',
                'placeholder.email': 'Enter your email',
                'placeholder.phone': '(11) 99999-9999',
                'placeholder.message': 'Enter your message',
                'placeholder.search': 'Type to search...',
                'placeholder.select': 'Select an option',
                'placeholder.date': 'DD/MM/YYYY',
                'placeholder.time': 'HH:MM',
                'placeholder.url': 'https://example.com',
                'placeholder.password': 'Enter your password',
                'placeholder.confirm_password': 'Confirm your password',
                
                // Titles and headers
                'title.contact': 'Contact Us',
                'title.newsletter': 'Newsletter',
                'title.login': 'Login',
                'title.register': 'Register',
                'title.profile': 'Profile',
                'title.settings': 'Settings',
                'title.help': 'Help',
                'title.about': 'About',
                'title.terms': 'Terms of Use',
                'title.privacy': 'Privacy Policy',
                'title.cookies': 'Cookie Policy',
                
                // Site specific messages
                'site.lead_form_title': 'Consult one of our specialists at no cost',
                'site.newsletter_title': 'Receive our insights',
                'site.newsletter_subtitle': 'Stay up to date with the best digital marketing strategies.',
                'site.contact_success': 'Message sent successfully! Our team will contact you soon.',
                'site.newsletter_success': 'Subscription successful! You will receive our insights soon.',
                'site.modal_title': 'Talk to the Specialist',
                'site.step1_title': "Let's start! Tell us about yourself",
                'site.step2_title': 'Tell us more about your business',
                'site.step3_title': 'Schedule your strategic meeting',
                'site.step4_title': 'Scheduling Complete!',
            },
            'es': {
                // Validaciones de formulario
                'validation.required': 'Este campo es obligatorio.',
                'validation.email': 'Por favor, ingrese un email válido.',
                'validation.phone': 'Por favor, ingrese un teléfono válido.',
                'validation.min_length': 'Este campo debe tener al menos {min} caracteres.',
                'validation.max_length': 'Este campo debe tener máximo {max} caracteres.',
                'validation.numeric': 'Este campo debe contener solo números.',
                'validation.alpha': 'Este campo debe contener solo letras.',
                'validation.alpha_numeric': 'Este campo debe contener solo letras y números.',
                'validation.url': 'Por favor, ingrese una URL válida.',
                'validation.date': 'Por favor, ingrese una fecha válida.',
                'validation.time': 'Por favor, ingrese una hora válida.',
                'validation.credit_card': 'Por favor, ingrese un número de tarjeta válido.',
                'validation.cpf': 'Por favor, ingrese un CPF válido.',
                'validation.cnpj': 'Por favor, ingrese un CNPJ válido.',
                'validation.cep': 'Por favor, ingrese un código postal válido.',
                
                // Mensajes de éxito
                'success.form_saved': '¡Datos guardados exitosamente!',
                'success.newsletter_subscribed': '¡Suscripción exitosa!',
                'success.contact_sent': '¡Mensaje enviado exitosamente!',
                'success.file_uploaded': '¡Archivo subido exitosamente!',
                'success.data_updated': '¡Datos actualizados exitosamente!',
                
                // Mensajes de error
                'error.generic': 'Ocurrió un error inesperado. Intente nuevamente.',
                'error.network': 'Error de conexión. Verifique su internet.',
                'error.server': 'Error interno del servidor. Intente más tarde.',
                'error.validation': 'Por favor, corrija los errores en el formulario.',
                'error.required_fields': 'Por favor, complete todos los campos obligatorios.',
                'error.invalid_data': 'Datos inválidos. Verifique la información.',
                'error.duplicate_email': 'Este email ya está registrado.',
                'error.invalid_credentials': 'Credenciales inválidas.',
                'error.session_expired': 'Su sesión ha expirado. Inicie sesión nuevamente.',
                
                // Mensajes de advertencia
                'warning.unsaved_changes': 'Tiene cambios sin guardar.',
                'warning.confirm_action': '¿Está seguro de que desea realizar esta acción?',
                'warning.data_loss': 'Esta acción puede causar pérdida de datos.',
                'warning.low_storage': 'Espacio de almacenamiento bajo.',
                'warning.maintenance': 'Sistema en mantenimiento. Intente más tarde.',
                
                // Mensajes informativos
                'info.loading': 'Cargando...',
                'info.saving': 'Guardando...',
                'info.processing': 'Procesando...',
                'info.uploading': 'Subiendo archivo...',
                'info.downloading': 'Descargando archivo...',
                'info.connecting': 'Conectando...',
                'info.disconnected': 'Desconectado.',
                'info.reconnecting': 'Reconectando...',
                
                // Etiquetas de formulario
                'form.name': 'Nombre',
                'form.email': 'Email',
                'form.phone': 'Teléfono',
                'form.message': 'Mensaje',
                'form.subject': 'Asunto',
                'form.company': 'Empresa',
                'form.website': 'Sitio Web',
                'form.address': 'Dirección',
                'form.city': 'Ciudad',
                'form.state': 'Estado',
                'form.zipcode': 'Código Postal',
                'form.country': 'País',
                'form.birth_date': 'Fecha de Nacimiento',
                'form.gender': 'Género',
                'form.newsletter': 'Newsletter',
                'form.terms': 'Términos y Condiciones',
                'form.privacy': 'Política de Privacidad',
                
                // Botones
                'button.save': 'Guardar',
                'button.cancel': 'Cancelar',
                'button.submit': 'Enviar',
                'button.send': 'Enviar',
                'button.close': 'Cerrar',
                'button.delete': 'Eliminar',
                'button.edit': 'Editar',
                'button.add': 'Agregar',
                'button.remove': 'Remover',
                'button.confirm': 'Confirmar',
                'button.back': 'Atrás',
                'button.next': 'Siguiente',
                'button.previous': 'Anterior',
                'button.finish': 'Finalizar',
                'button.continue': 'Continuar',
                'button.retry': 'Intentar Nuevamente',
                'button.refresh': 'Actualizar',
                'button.download': 'Descargar',
                'button.upload': 'Subir',
                'button.search': 'Buscar',
                'button.filter': 'Filtrar',
                'button.clear': 'Limpiar',
                'button.reset': 'Resetear',
                'button.load_more': 'Cargar Más',
                'button.show_more': 'Mostrar Más',
                'button.show_less': 'Mostrar Menos',
                
                // Placeholders
                'placeholder.name': 'Ingrese su nombre completo',
                'placeholder.email': 'Ingrese su email',
                'placeholder.phone': '(11) 99999-9999',
                'placeholder.message': 'Ingrese su mensaje',
                'placeholder.search': 'Escriba para buscar...',
                'placeholder.select': 'Seleccione una opción',
                'placeholder.date': 'DD/MM/AAAA',
                'placeholder.time': 'HH:MM',
                'placeholder.url': 'https://ejemplo.com',
                'placeholder.password': 'Ingrese su contraseña',
                'placeholder.confirm_password': 'Confirme su contraseña',
                
                // Títulos y encabezados
                'title.contact': 'Contáctanos',
                'title.newsletter': 'Newsletter',
                'title.login': 'Iniciar Sesión',
                'title.register': 'Registrarse',
                'title.profile': 'Perfil',
                'title.settings': 'Configuración',
                'title.help': 'Ayuda',
                'title.about': 'Acerca de',
                'title.terms': 'Términos de Uso',
                'title.privacy': 'Política de Privacidad',
                'title.cookies': 'Política de Cookies',
                
                // Mensajes específicos del sitio
                'site.lead_form_title': 'Consulte a uno de nuestros especialistas sin costo',
                'site.newsletter_title': 'Reciba nuestros insights',
                'site.newsletter_subtitle': 'Manténgase al día con las mejores estrategias de marketing digital.',
                'site.contact_success': '¡Mensaje enviado exitosamente! Nuestro equipo se pondrá en contacto pronto.',
                'site.newsletter_success': '¡Suscripción exitosa! Recibirá nuestros insights pronto.',
                'site.modal_title': 'Hable con el Especialista',
                'site.step1_title': '¡Empecemos! Cuéntanos sobre ti',
                'site.step2_title': 'Cuéntanos más sobre tu negocio',
                'site.step3_title': 'Programa tu reunión estratégica',
                'site.step4_title': '¡Programación Completa!',
            }
        };
    }

    /**
     * Detecta o idioma atual baseado no navegador ou configuração
     */
    detectLanguage() {
        // Verificar se há idioma salvo no localStorage
        const savedLanguage = localStorage.getItem('preferred_language');
        if (savedLanguage && this.translations[savedLanguage]) {
            return savedLanguage;
        }

        // Verificar idioma do navegador
        const browserLanguage = navigator.language || navigator.userLanguage;
        if (browserLanguage.startsWith('pt')) {
            return 'pt-br';
        } else if (browserLanguage.startsWith('en')) {
            return 'en';
        } else if (browserLanguage.startsWith('es')) {
            return 'es';
        }

        // Verificar subdomínio
        const hostname = window.location.hostname;
        if (hostname.startsWith('en.')) {
            return 'en';
        } else if (hostname.startsWith('es.')) {
            return 'es';
        }

        // Padrão: português brasileiro
        return 'pt-br';
    }

    /**
     * Define o idioma atual
     * @param {string} language - Código do idioma
     */
    setLanguage(language) {
        if (this.translations[language]) {
            this.currentLanguage = language;
            localStorage.setItem('preferred_language', language);
            this.updatePageLanguage();
        }
    }

    /**
     * Atualiza o idioma da página
     */
    updatePageLanguage() {
        document.documentElement.lang = this.currentLanguage;
        
        // Disparar evento customizado para notificar mudança de idioma
        window.dispatchEvent(new CustomEvent('languageChanged', {
            detail: { language: this.currentLanguage }
        }));
    }

    /**
     * Traduz uma chave
     * @param {string} key - Chave da tradução
     * @param {Object} params - Parâmetros para substituição
     * @returns {string} Texto traduzido
     */
    t(key, params = {}) {
        const translation = this.translations[this.currentLanguage][key] || 
                          this.translations['pt-br'][key] || 
                          key;

        // Substituir parâmetros no formato {param}
        return translation.replace(/\{(\w+)\}/g, (match, param) => {
            return params[param] || match;
        });
    }

    /**
     * Traduz e formata um texto
     * @param {string} key - Chave da tradução
     * @param {Object} params - Parâmetros para substituição
     * @returns {string} Texto traduzido e formatado
     */
    format(key, params = {}) {
        return this.t(key, params);
    }

    /**
     * Obtém o idioma atual
     * @returns {string} Código do idioma atual
     */
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    /**
     * Obtém todos os idiomas disponíveis
     * @returns {Array} Lista de idiomas disponíveis
     */
    getAvailableLanguages() {
        return Object.keys(this.translations);
    }

    /**
     * Verifica se um idioma está disponível
     * @param {string} language - Código do idioma
     * @returns {boolean} True se disponível
     */
    isLanguageAvailable(language) {
        return this.translations.hasOwnProperty(language);
    }
}

// Instância global
window.i18n = new I18n();

// Métodos globais para compatibilidade
window.t = (key, params) => window.i18n.t(key, params);
window.setLanguage = (language) => window.i18n.setLanguage(language);
window.getCurrentLanguage = () => window.i18n.getCurrentLanguage();

// Auto-inicialização
document.addEventListener('DOMContentLoaded', function() {
    window.i18n.updatePageLanguage();
});

// Exportar para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = I18n;
}
