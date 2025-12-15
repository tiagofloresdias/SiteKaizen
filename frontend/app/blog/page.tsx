import { Metadata } from 'next'
import Link from 'next/link'
import Image from 'next/image'
import { getArticles, Article } from '@/lib/api'
import Breadcrumb from '@/components/seo/Breadcrumb'

export const metadata: Metadata = {
  title: 'Blog',
  description: 'Artigos sobre marketing digital, SEO, mídia paga, automação e estratégias para acelerar seu negócio.',
}

export default async function BlogPage() {
  let articles: Article[] = []
  try {
    const articlesResponse = await getArticles({ is_published: true, limit: 50 })
    articles = articlesResponse.data || []
  } catch (error) {
    console.warn('Erro ao buscar artigos:', error)
    articles = []
  }

  const breadcrumbItems = [
    { name: 'Home', url: '/' },
    { name: 'Aprenda Marketing', url: '/aprenda-marketing' },
  ]

  return (
    <div className="pt-20 min-h-screen bg-black">
      {/* Hero Section */}
      <section className="py-16 border-b border-ka-border">
        <div className="container mx-auto px-4">
          <Breadcrumb items={breadcrumbItems} />
          <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
            Blog
          </h1>
          <p className="text-lg text-text-muted max-w-3xl">
            Artigos sobre marketing digital, SEO, mídia paga, automação e estratégias para acelerar seu negócio.
          </p>
        </div>
      </section>

      {/* Articles Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          {articles.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-text-muted text-lg">
                Nenhum artigo publicado no momento.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {articles.map((article) => (
                <Link
                  key={article.id}
                  href={`/aprenda-marketing/${article.slug}`}
                  className="ka-card p-6 block group"
                >
                  {article.cover_image_url && (
                    <div className="mb-4 overflow-hidden rounded-lg">
                      <Image
                        src={article.cover_image_url}
                        alt={article.title}
                        width={400}
                        height={250}
                        className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  )}
                  {article.category && (
                    <span className="inline-block text-xs text-primary font-medium mb-2">
                      {article.category.name}
                    </span>
                  )}
                  <h3 className="text-xl font-bold text-white mb-2 group-hover:text-primary transition-colors line-clamp-2">
                    {article.title}
                  </h3>
                  {article.excerpt && (
                    <p className="text-text-muted mb-4 line-clamp-3">{article.excerpt}</p>
                  )}
                  <div className="flex items-center justify-between text-sm text-text-muted">
                    {article.published_at && (
                      <time dateTime={article.published_at}>
                        {new Date(article.published_at).toLocaleDateString('pt-BR', {
                          day: 'numeric',
                          month: 'long',
                          year: 'numeric',
                        })}
                      </time>
                    )}
                    {article.reading_time && (
                      <span>{article.reading_time} min de leitura</span>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

