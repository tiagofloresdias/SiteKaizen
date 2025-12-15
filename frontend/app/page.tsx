import Link from 'next/link'
import Image from 'next/image'
import { generateOrganizationSchema } from '@/components/seo/JsonLd'

export default function HomePage() {
  const organizationSchema = generateOrganizationSchema()

  return (
    <>
      {/* JSON-LD Organization */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />

      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden bg-black">
        {/* Background Image */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-fixed"
          style={{
            backgroundImage: "url('/img/backgrounds/fundo-site-kaizen.webp')",
            filter: 'brightness(0.35) saturate(1.1) contrast(1.05)',
            transform: 'scale(1.05)',
          }}
        />
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/40 to-black/60" />
        
        {/* Pink Gradient Overlay */}
        <div
          className="absolute inset-0"
          style={{
            background: 'radial-gradient(ellipse at 30% 20%, rgba(234,0,41,.18), transparent 40%), radial-gradient(ellipse at 70% 80%, rgba(234,0,41,.12), transparent 45%)',
            pointerEvents: 'none',
          }}
        />

        {/* Content */}
        <div className="relative z-10 container mx-auto px-4 text-center">
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-white mb-6 drop-shadow-2xl">
            Aceleramos negócios<br />
            <span className="text-gradient">e lançamos foguetes</span>
          </h1>
          <p className="text-xl md:text-2xl text-white/85 mb-8 max-w-3xl mx-auto">
            Desde 2015, ajudamos empresas a crescer com estratégias afiadas, dados precisos e um time de elite. 
            Se sua meta é escalar, nós temos o combustível.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/contato" className="btn-primary text-lg px-8 py-4">
              Quero vender +
            </Link>
            <Link href="/solucoes" className="btn-outline text-lg px-8 py-4">
              Ver soluções
            </Link>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="py-20 bg-black">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-6">
              não somos apenas uma agência.
            </h2>
            <h3 className="text-3xl md:text-4xl font-bold text-primary mb-8">
              Somos uma aceleradora de vendas.
            </h3>
            <p className="text-lg text-text-muted mb-8 leading-relaxed">
              O Grupo Kaizen nasceu para desafiar o comum. Fomos pioneiros em Inside Sales no Brasil e crescemos 
              até nos tornarmos Google Partner Premier. Em poucos anos, ajudamos mais de 1.000 empresas a escalar. 
              Não acreditamos em fórmulas prontas. Criamos estratégias personalizadas para levar negócios ao próximo nível.
            </p>
            <Link href="/nossas-empresas" className="btn-primary">
              Conheça nossa história
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary/10 to-primary-light/10">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-6">
            Avaliação Gratuita
          </h2>
          <p className="text-xl text-text-muted mb-8 max-w-2xl mx-auto">
            Consulte um dos nossos especialistas sem nenhum custo
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="tel:08005508000" className="btn-primary text-lg px-8 py-4">
              📞 0800-550-8000
            </a>
            <Link href="/contato" className="btn-outline text-lg px-8 py-4">
              Fale Conosco
            </Link>
          </div>
        </div>
      </section>
    </>
  )
}



