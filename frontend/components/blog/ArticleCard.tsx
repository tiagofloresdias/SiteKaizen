import Image from 'next/image'
import Link from 'next/link'
import { Article } from '@/lib/api'

export default function ArticleCard({ article }: { article: Article }) {
  const publishedDate = article.published_at 
    ? new Date(article.published_at).toLocaleDateString('pt-BR', { 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
      })
    : null

  return (
    <article 
      className="ka-card p-6 group hover:border-primary/50 transition-all duration-300"
      itemScope
      itemType="https://schema.org/BlogPosting"
    >
      {article.cover_image_url && (
        <Link href={`/aprenda-marketing/${article.slug}`} className="block mb-4 overflow-hidden rounded-lg">
          <Image
            src={article.cover_image_url}
            alt={article.title}
            width={400}
            height={250}
            className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
            itemProp="image"
          />
        </Link>
      )}
      
      {article.category && (
        <div className="mb-3">
          <span className="inline-block px-3 py-1 bg-primary/20 text-primary text-xs font-semibold rounded-full uppercase tracking-wide">
            {article.category.name}
          </span>
        </div>
      )}

      <h2 className="text-xl font-bold text-white mb-3 group-hover:text-primary transition-colors line-clamp-2">
        <Link 
          href={`/aprenda-marketing/${article.slug}`}
          itemProp="headline"
        >
          {article.title}
        </Link>
      </h2>

      {article.excerpt && (
        <p 
          className="text-text-muted text-sm mb-4 line-clamp-3"
          itemProp="description"
        >
          {article.excerpt}
        </p>
      )}

      <div className="flex items-center justify-between mt-4">
        <div className="flex items-center gap-3 text-xs text-text-muted">
          {publishedDate && (
            <time dateTime={article.published_at} itemProp="datePublished">
              {publishedDate}
            </time>
          )}
          {article.reading_time && (
            <span>• {article.reading_time} min de leitura</span>
          )}
        </div>
        <Link
          href={`/aprenda-marketing/${article.slug}`}
          className="text-primary hover:text-primary-light transition-colors flex items-center gap-1 group/link"
          aria-label={`Ler artigo: ${article.title}`}
        >
          <span className="text-sm font-medium">Ler mais</span>
          <svg 
            className="w-4 h-4 transform group-hover/link:translate-x-1 transition-transform" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>

      <meta itemProp="author" content="Agência Kaizen" />
      <meta itemProp="publisher" content="Universidade Kaizen" />
    </article>
  )
}

