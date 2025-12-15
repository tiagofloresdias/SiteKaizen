import { Metadata } from 'next'
import Breadcrumb from '@/components/seo/Breadcrumb'
import { generateOrganizationSchema } from '@/components/seo/JsonLd'

export const metadata: Metadata = {
  title: 'Contato',
  description: 'Entre em contato com a Agência Kaizen. Avaliação gratuita com nossos especialistas.',
}

export default function ContatoPage() {
  const breadcrumbItems = [
    { name: 'Home', url: '/' },
    { name: 'Contato', url: '/contato' },
  ]

  const organizationSchema = generateOrganizationSchema()

  return (
    <>
      {/* JSON-LD Organization */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />

      <div className="pt-20 min-h-screen bg-black">
        {/* Hero Section */}
        <section className="py-16 border-b border-ka-border">
          <div className="container mx-auto px-4">
            <Breadcrumb items={breadcrumbItems} />
            <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
              Fale Conosco
            </h1>
            <p className="text-lg text-text-muted max-w-3xl">
              Consulte um dos nossos especialistas sem nenhum custo. Preencha o formulário ou entre em contato diretamente.
            </p>
          </div>
        </section>

        {/* Contact Section */}
        <section className="py-16">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
              {/* Contact Info */}
              <div>
                <h2 className="text-3xl font-bold text-white mb-8">
                  Entre em contato
                </h2>
                
                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                      <span className="mr-3 text-2xl">📞</span>
                      Telefone
                    </h3>
                    <a
                      href="tel:08005508000"
                      className="text-primary hover:underline text-lg"
                    >
                      0800-550-8000
                    </a>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                      <span className="mr-3 text-2xl">✉️</span>
                      E-mail
                    </h3>
                    <a
                      href="mailto:contato@agenciakaizen.com.br"
                      className="text-primary hover:underline text-lg"
                    >
                      contato@agenciakaizen.com.br
                    </a>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                      <span className="mr-3 text-2xl">💬</span>
                      WhatsApp
                    </h3>
                    <a
                      href="https://wa.me/5508005508000?text=Olá! Vim pelo site da Agência Kaizen e gostaria de saber mais sobre os serviços."
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline text-lg"
                    >
                      Chame no WhatsApp
                    </a>
                  </div>
                </div>

                <div className="mt-12">
                  <h3 className="text-xl font-bold text-white mb-4">
                    Horário de Atendimento
                  </h3>
                  <p className="text-text-muted">
                    Segunda a Sexta: 9h às 18h
                  </p>
                </div>
              </div>

              {/* Contact Form Placeholder */}
              <div className="ka-card p-8">
                <h2 className="text-2xl font-bold text-white mb-6">
                  Envie sua mensagem
                </h2>
                <p className="text-text-muted mb-6">
                  Preencha o formulário abaixo e nossa equipe entrará em contato em breve.
                </p>
                
                <form className="space-y-4">
                  <div>
                    <label htmlFor="name" className="block text-white font-medium mb-2">
                      Nome *
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      required
                      className="w-full px-4 py-3 bg-ka-dark-2 border border-ka-border rounded-lg text-white placeholder-text-muted focus:outline-none focus:border-primary transition-colors"
                      placeholder="Seu nome completo"
                    />
                  </div>

                  <div>
                    <label htmlFor="email" className="block text-white font-medium mb-2">
                      E-mail *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      required
                      className="w-full px-4 py-3 bg-ka-dark-2 border border-ka-border rounded-lg text-white placeholder-text-muted focus:outline-none focus:border-primary transition-colors"
                      placeholder="seu@email.com"
                    />
                  </div>

                  <div>
                    <label htmlFor="phone" className="block text-white font-medium mb-2">
                      Telefone
                    </label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      className="w-full px-4 py-3 bg-ka-dark-2 border border-ka-border rounded-lg text-white placeholder-text-muted focus:outline-none focus:border-primary transition-colors"
                      placeholder="(00) 00000-0000"
                    />
                  </div>

                  <div>
                    <label htmlFor="message" className="block text-white font-medium mb-2">
                      Mensagem *
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      rows={5}
                      required
                      className="w-full px-4 py-3 bg-ka-dark-2 border border-ka-border rounded-lg text-white placeholder-text-muted focus:outline-none focus:border-primary transition-colors resize-none"
                      placeholder="Conte-nos sobre seu negócio e desafios..."
                    />
                  </div>

                  <button
                    type="submit"
                    className="btn-primary w-full text-lg py-4"
                  >
                    Enviar Mensagem
                  </button>
                </form>

                <p className="text-xs text-text-muted mt-4">
                  * Campos obrigatórios
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </>
  )
}



