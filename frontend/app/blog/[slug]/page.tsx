import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'
import { getArticleBySlug, getArticles } from '@/lib/api'
import Breadcrumb from '@/components/seo/Breadcrumb'
import { generateArticleSchema } from '@/components/seo/JsonLd'

interface PageProps {
  params: {
    slug: string
  }
}

export async function generateStaticParams() {
  try {
    const articles = await getArticles({ is_published: true, limit: 100 })
    return articles.data.map((article) => ({
      slug: article.slug,
    }))
  } catch (error) {
    // Durante build, se API não estiver disponível, retornar array vazio
    console.warn('API não disponível durante build, usando rotas dinâmicas')
    return []
  }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  try {
    const article = await getArticleBySlug(params.slug)
    return {
      title: article.seo_title || article.title,
      description: article.seo_description || article.excerpt || article.title,
      keywords: article.meta_keywords?.split(',') || [],
      openGraph: {
        title: article.title,
        description: article.excerpt || article.title,
        type: 'article',
        images: article.cover_image_url ? [article.cover_image_url] : undefined,
        publishedTime: article.published_at || undefined,
        modifiedTime: article.updated_at || undefined,
      },
      twitter: {
        card: 'summary_large_image',
        title: article.title,
        description: article.excerpt || article.title,
        images: article.social_image_url || article.cover_image_url ? [article.social_image_url || article.cover_image_url || ''] : undefined,
      },
    }
  } catch {
    return {
      title: 'Artigo não encontrado',
    }
  }
}

export default async function ArticlePage({ params }: PageProps) {
  let article
  try {
    article = await getArticleBySlug(params.slug)
  } catch {
    notFound()
  }

  const breadcrumbItems = [
    { name: 'Home', url: '/' },
    { name: 'Blog', url: '/blog' },
    { name: article.title },
  ]

  // JSON-LD Article
  const articleSchema = generateArticleSchema({
    title: article.title,
    description: article.excerpt || article.title,
    image: article.cover_image_url || article.social_image_url,
    publishedAt: article.published_at || article.created_at,
    updatedAt: article.updated_at || article.published_at || article.created_at,
    slug: article.slug,
  })

  return (
    <>
      {/* JSON-LD Article */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
      />

      <article className="pt-20 min-h-screen bg-black">
        {/* Hero */}
        <section className="py-16 border-b border-ka-border">
          <div className="container mx-auto px-4 max-w-4xl">
            <Breadcrumb items={breadcrumbItems} />
            
            {article.cover_image_url && (
              <div className="mb-8 overflow-hidden rounded-2xl">
                <Image
                  src={article.cover_image_url}
                  alt={article.title}
                  width={1200}
                  height={630}
                  className="w-full h-auto"
                  priority
                />
              </div>
            )}

            <header>
              {article.category && (
                <span className="inline-block text-sm text-primary font-medium mb-4">
                  {article.category.name}
                </span>
              )}
              <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
                {article.title}
              </h1>
              {article.excerpt && (
                <p className="text-xl text-text-muted mb-6">{article.excerpt}</p>
              )}
              <div className="flex items-center gap-6 text-sm text-text-muted">
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
            </header>
          </div>
        </section>

        {/* Content */}
        <section className="py-16">
          <div className="container mx-auto px-4 max-w-4xl">
            <div
              className="prose prose-invert prose-lg max-w-none
                prose-headings:text-white prose-headings:font-bold
                prose-p:text-text-muted prose-p:leading-relaxed
                prose-a:text-primary prose-a:no-underline hover:prose-a:underline
                prose-strong:text-white prose-strong:font-bold
                prose-img:rounded-lg prose-img:w-full
                prose-ul:text-text-muted prose-ol:text-text-muted
                prose-li:text-text-muted"
              dangerouslySetInnerHTML={{ __html: article.content }}
            />
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 bg-gradient-to-r from-primary/10 to-primary-light/10">
          <div className="container mx-auto px-4 text-center max-w-4xl">
            <h2 className="text-3xl font-bold text-white mb-4">
              Quer acelerar seu negócio?
            </h2>
            <p className="text-lg text-text-muted mb-8 max-w-2xl mx-auto">
              Entre em contato com nossos especialistas e descubra como podemos ajudar.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contato" className="btn-primary text-lg px-8 py-4">
                Fale Conosco
              </Link>
              <Link href="/blog" className="btn-outline text-lg px-8 py-4">
                Ver Mais Artigos
              </Link>
            </div>
          </div>
        </section>
      </article>
    </>
  )
}

