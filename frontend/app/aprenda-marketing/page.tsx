import { Metadata } from 'next'
import Link from 'next/link'
import { getArticles, Article } from '@/lib/api'
import Breadcrumb from '@/components/seo/Breadcrumb'
import { generateOrganizationSchema } from '@/components/seo/JsonLd'
import ArticleCard from '@/components/blog/ArticleCard'
import LoadMoreArticles from '@/components/blog/LoadMoreArticles'

export const metadata: Metadata = {
  title: 'Aprenda Marketing - Universidade Kaizen | Educação Aberta em Marketing Digital',
  description: 'Aprenda marketing digital, vendas e inovação com especialistas. Cursos gratuitos, artigos, cases e estratégias que realmente funcionam no mercado. Educação aberta da Universidade Kaizen.',
  keywords: 'aprender marketing digital, cursos marketing, educação marketing, universidade kaizen, estratégias marketing, vendas, inovação digital',
  openGraph: {
    title: 'Aprenda Marketing - Universidade Kaizen',
    description: 'Educação aberta em marketing digital, vendas e inovação. Aprenda com especialistas e descubra táticas que realmente funcionam.',
    type: 'website',
    url: 'https://site2025.agenciakaizen.com.br/aprenda-marketing',
  },
  alternates: {
    canonical: 'https://site2025.agenciakaizen.com.br/aprenda-marketing',
  },
}

// Componente de CTA Universidade Kaizen
function UniversidadeKaizenCTA() {
  return (
    <section className="py-16 bg-gradient-to-r from-primary/10 via-primary/5 to-primary-light/10 border-y border-primary/20">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
                Universidade Kaizen
              </h2>
              <p className="text-2xl font-bold text-primary mb-6">
                Evolução contínua para performance máxima
              </p>
              <div className="space-y-4 text-text-muted text-lg leading-relaxed">
                <p>
                  A <strong className="text-white">Universidade Kaizen</strong> é nossa plataforma de educação aberta, 
                  criada para formar estrategistas de alta performance em vendas, marketing e automação de processos.
                </p>
                <p>
                  Oferecemos <strong className="text-white">cursos gratuitos</strong>, trilhas de aprendizado completas 
                  e conteúdo exclusivo para profissionais que querem dominar as melhores práticas do mercado.
                </p>
                <p>
                  Junte-se a centenas de profissionais que já transformaram suas carreiras com nossa metodologia comprovada.
                </p>
              </div>
              <Link
                href="https://universidade.agenciakaizen.com.br"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block mt-8 btn-primary text-lg px-8 py-4"
              >
                Quero participar →
              </Link>
            </div>
            <div className="relative">
              <div className="grid grid-cols-2 gap-4">
                <div className="ka-card p-4 bg-dark-2">
                  <div className="text-primary text-3xl font-bold mb-2">100+</div>
                  <div className="text-text-muted text-sm">Cursos Gratuitos</div>
                </div>
                <div className="ka-card p-4 bg-dark-2">
                  <div className="text-primary text-3xl font-bold mb-2">500+</div>
                  <div className="text-text-muted text-sm">Profissionais Formados</div>
                </div>
                <div className="ka-card p-4 bg-dark-2">
                  <div className="text-primary text-3xl font-bold mb-2">24/7</div>
                  <div className="text-text-muted text-sm">Acesso Ilimitado</div>
                </div>
                <div className="ka-card p-4 bg-dark-2">
                  <div className="text-primary text-3xl font-bold mb-2">100%</div>
                  <div className="text-text-muted text-sm">Gratuito</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default async function AprendaMarketingPage() {
  let articles: Article[] = []
  let total = 0
  
  try {
    const response = await getArticles({ 
      is_published: true, 
      limit: 12 
    })
    articles = response.data || []
    total = response.total || 0
  } catch (error) {
    console.warn('Erro ao buscar artigos:', error)
  }

  // Dados estruturados para Blog
  const blogSchema = {
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "Aprenda Marketing - Universidade Kaizen",
    "description": "Educação aberta em marketing digital, vendas e inovação. Aprenda com especialistas e descubra táticas que realmente funcionam no mercado.",
    "url": "https://site2025.agenciakaizen.com.br/aprenda-marketing",
    "publisher": {
      "@type": "Organization",
      "name": "Universidade Kaizen",
      "url": "https://universidade.agenciakaizen.com.br",
      "logo": {
        "@type": "ImageObject",
        "url": "https://site2025.agenciakaizen.com.br/img/logos/logo-kaizen-maior.webp"
      }
    },
    "blogPost": articles.slice(0, 10).map(article => ({
      "@type": "BlogPosting",
      "headline": article.title,
      "description": article.excerpt || article.seo_description || "",
      "image": article.cover_image_url || article.social_image_url || "",
      "datePublished": article.published_at,
      "dateModified": article.updated_at || article.published_at,
      "author": {
        "@type": "Organization",
        "name": "Agência Kaizen"
      },
      "publisher": {
        "@type": "Organization",
        "name": "Universidade Kaizen",
        "logo": {
          "@type": "ImageObject",
          "url": "https://site2025.agenciakaizen.com.br/img/logos/logo-kaizen-maior.webp"
        }
      },
      "url": `https://site2025.agenciakaizen.com.br/aprenda-marketing/${article.slug}`,
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": `https://site2025.agenciakaizen.com.br/aprenda-marketing/${article.slug}`
      }
    }))
  }

  const breadcrumbItems = [
    { name: 'Home', url: '/' },
    { name: 'Aprenda Marketing', url: '/aprenda-marketing' },
  ]

  return (
    <>
      {/* Dados Estruturados - Blog */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(blogSchema) }}
      />
      
      {/* Dados Estruturados - Organization */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateOrganizationSchema()) }}
      />

      <div className="pt-20 min-h-screen bg-black">
        {/* Hero Section */}
        <section className="py-16 border-b border-ka-border bg-gradient-to-b from-black via-dark-1 to-black">
          <div className="container mx-auto px-4">
            <Breadcrumb items={breadcrumbItems} />
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-white mb-6">
                Transforme seu conhecimento em resultados
              </h1>
              <p className="text-xl md:text-2xl text-text-muted mb-8 leading-relaxed">
                Aqui você encontra tudo sobre estratégias de marketing, vendas e inovação digital. 
                Aprenda com especialistas e descubra táticas que realmente funcionam no mercado.
              </p>
              <div className="flex flex-wrap gap-4 justify-center text-sm text-text-muted">
                <span className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  Educação Aberta
                </span>
                <span className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  {total}+ Artigos
                </span>
                <span className="flex items-center gap-2">
                  <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  Especialistas
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* Artigos Grid */}
        <section className="py-16">
          <div className="container mx-auto px-4">
            {articles.length === 0 ? (
              <div className="text-center py-20">
                <p className="text-text-muted text-lg">
                  Nenhum conteúdo disponível no momento.
                </p>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
                  {articles.map((article) => (
                    <ArticleCard key={article.id} article={article} />
                  ))}
                  
                  {/* Carregamento Progressivo */}
                  {total > articles.length && (
                    <LoadMoreArticles
                      initialArticles={articles}
                      total={total}
                      apiEndpoint="/api/v1/articles"
                    />
                  )}
                </div>
              </>
            )}
          </div>
        </section>

        {/* CTA Universidade Kaizen */}
        <UniversidadeKaizenCTA />
      </div>
    </>
  )
}

