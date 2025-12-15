'use client'

import { useState, useEffect, useRef } from 'react'
import { Article, getArticles } from '@/lib/api'
import ArticleCard from './ArticleCard'

interface LoadMoreArticlesProps {
  initialArticles: Article[]
  total: number
  apiEndpoint: string
}

export default function LoadMoreArticles({ 
  initialArticles, 
  total, 
  apiEndpoint 
}: LoadMoreArticlesProps) {
  const [articles, setArticles] = useState<Article[]>(initialArticles)
  const [loading, setLoading] = useState(false)
  const [hasMore, setHasMore] = useState(initialArticles.length < total)
  const [page, setPage] = useState(2)
  const observerRef = useRef<IntersectionObserver | null>(null)
  const triggerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Intersection Observer para carregamento automático ao scroll
    if (typeof window !== 'undefined' && 'IntersectionObserver' in window) {
      observerRef.current = new IntersectionObserver(
        (entries) => {
          const first = entries[0]
          if (first.isIntersecting && hasMore && !loading) {
            loadMore()
          }
        },
        { threshold: 0.1, rootMargin: '100px' }
      )

      if (triggerRef.current) {
        observerRef.current.observe(triggerRef.current)
      }
    }

    return () => {
      if (observerRef.current && triggerRef.current) {
        observerRef.current.unobserve(triggerRef.current)
      }
    }
  }, [hasMore, loading])

  const loadMore = async () => {
    if (loading || !hasMore) return

    setLoading(true)
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://site2025.agenciakaizen.com.br/api/v1'
      const response = await fetch(`${API_BASE_URL}${apiEndpoint}?page=${page}&limit=12&is_published=true`)
      if (response.ok) {
        const data = await response.json()
        const newArticles = data.data || []
        
        if (newArticles.length > 0) {
          setArticles(prev => [...prev, ...newArticles])
          setPage(prev => prev + 1)
          setHasMore(articles.length + newArticles.length < total)
        } else {
          setHasMore(false)
        }
      }
    } catch (error) {
      console.error('Erro ao carregar mais artigos:', error)
      setHasMore(false)
    } finally {
      setLoading(false)
    }
  }

  if (!hasMore) return null

  return (
    <>
      {articles.slice(initialArticles.length).map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
      
      <div ref={triggerRef} className="col-span-full h-20 flex items-center justify-center">
        {loading && (
          <div className="flex items-center gap-2 text-primary">
            <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <span>Carregando mais artigos...</span>
          </div>
        )}
      </div>
    </>
  )
}

