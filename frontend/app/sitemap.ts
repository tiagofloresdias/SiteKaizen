import { MetadataRoute } from 'next'
import { getSitemapData } from '@/lib/api'

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://site2025.agenciakaizen.com.br'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  try {
    const sitemapData = await getSitemapData().catch(() => ({
      companies: [],
      articles: [],
      static_pages: ['/', '/nossas-empresas', '/blog', '/onde-estamos', '/contato'],
    }))

    const staticPages: MetadataRoute.Sitemap = sitemapData.static_pages.map((path) => ({
      url: `${siteUrl}${path}`,
      lastModified: new Date(),
      changeFrequency: path === '/' ? 'daily' : 'weekly',
      priority: path === '/' ? 1 : 0.8,
    }))

    const companyPages: MetadataRoute.Sitemap = sitemapData.companies.map((slug) => ({
      url: `${siteUrl}/nossas-empresas/${slug}`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.7,
    }))

    const articlePages: MetadataRoute.Sitemap = sitemapData.articles.map((slug) => ({
      url: `${siteUrl}/blog/${slug}`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.6,
    }))

    return [...staticPages, ...companyPages, ...articlePages]
  } catch (error) {
    console.error('Error generating sitemap:', error)
    // Fallback para páginas estáticas se a API falhar
    return [
      {
        url: siteUrl,
        lastModified: new Date(),
        changeFrequency: 'daily',
        priority: 1,
      },
      {
        url: `${siteUrl}/nossas-empresas`,
        lastModified: new Date(),
        changeFrequency: 'weekly',
        priority: 0.8,
      },
      {
        url: `${siteUrl}/blog`,
        lastModified: new Date(),
        changeFrequency: 'weekly',
        priority: 0.8,
      },
      {
        url: `${siteUrl}/onde-estamos`,
        lastModified: new Date(),
        changeFrequency: 'monthly',
        priority: 0.7,
      },
      {
        url: `${siteUrl}/contato`,
        lastModified: new Date(),
        changeFrequency: 'monthly',
        priority: 0.7,
      },
    ]
  }
}

