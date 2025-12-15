/**
 * Helpers para JSON-LD (Schema.org)
 */

export interface OrganizationSchema {
  '@context': 'https://schema.org'
  '@type': 'Organization'
  '@id'?: string
  name: string
  url: string
  logo: string
  image?: string
  description?: string
  contactPoint?: {
    '@type': 'ContactPoint'
    telephone: string
    contactType: string
    email?: string
  }
  sameAs?: string[]
}

export interface LocalBusinessSchema {
  '@context': 'https://schema.org'
  '@type': 'LocalBusiness'
  '@id'?: string
  name: string
  description?: string
  url: string
  telephone?: string
  email?: string
  logo?: string
  image?: string
  address: {
    '@type': 'PostalAddress'
    streetAddress: string
    addressLocality: string
    addressRegion: string
    postalCode?: string
    addressCountry: string
  }
  geo?: {
    '@type': 'GeoCoordinates'
    latitude: number
    longitude: number
  }
  openingHours?: string
}

export interface ArticleSchema {
  '@context': 'https://schema.org'
  '@type': 'Article' | 'BlogPosting'
  '@id'?: string
  headline: string
  description?: string
  image?: string
  datePublished: string
  dateModified?: string
  author: {
    '@type': 'Organization'
    name: string
    url?: string
  }
  publisher: {
    '@type': 'Organization'
    name: string
    logo: {
      '@type': 'ImageObject'
      url: string
    }
  }
}

export interface BreadcrumbListSchema {
  '@context': 'https://schema.org'
  '@type': 'BreadcrumbList'
  itemListElement: Array<{
    '@type': 'ListItem'
    position: number
    name: string
    item?: string
  }>
}

/**
 * Gera schema Organization global da Kaizen
 */
export function generateOrganizationSchema(): OrganizationSchema {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://site2025.agenciakaizen.com.br'
  
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': `${siteUrl}#organization`,
    name: 'Agência Kaizen',
    url: siteUrl,
    logo: `${siteUrl}/img/logos/logo-kaizen-maior.webp`,
    image: `${siteUrl}/img/logos/logo-kaizen-maior.webp`,
    description: 'Agência Kaizen - Marketing Digital de Alta Performance. Aceleramos negócios e lançamos foguetes.',
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+55-0800-550-8000',
      contactType: 'customer service',
      email: 'contato@agenciakaizen.com.br',
    },
    sameAs: [
      'https://www.linkedin.com/company/agenciakaizen/',
      'https://www.instagram.com/agenciakaizen/',
    ],
  }
}

/**
 * Gera schema LocalBusiness para uma localização
 */
export function generateLocalBusinessSchema(location: {
  name: string
  city: string
  state: string
  address: string
  postal_code?: string
  country: string
  phone?: string
  email?: string
  latitude?: number
  longitude?: number
  opening_hours?: string
}): LocalBusinessSchema {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://site2025.agenciakaizen.com.br'
  
  const schema: LocalBusinessSchema = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    '@id': `${siteUrl}/onde-estamos/#${location.city.toLowerCase().replace(' ', '-')}`,
    name: `${location.name} - ${location.city}`,
    description: 'Agência Kaizen - Marketing Digital de Alta Performance',
    url: `${siteUrl}/onde-estamos/`,
    telephone: location.phone || '',
    email: location.email || 'contato@agenciakaizen.com.br',
    logo: `${siteUrl}/img/logos/logo-kaizen-header.webp`,
    image: `${siteUrl}/img/logos/logo-kaizen-header.webp`,
    address: {
      '@type': 'PostalAddress',
      streetAddress: location.address,
      addressLocality: location.city,
      addressRegion: location.state,
      postalCode: location.postal_code || '',
      addressCountry: location.country,
    },
  }
  
  if (location.latitude && location.longitude) {
    schema.geo = {
      '@type': 'GeoCoordinates',
      latitude: location.latitude,
      longitude: location.longitude,
    }
  }
  
  if (location.opening_hours) {
    schema.openingHours = location.opening_hours
  }
  
  return schema
}

/**
 * Gera schema Article para um artigo do blog
 */
export function generateArticleSchema(article: {
  title: string
  description?: string
  image?: string
  publishedAt: string
  updatedAt?: string
  slug: string
}): ArticleSchema {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://site2025.agenciakaizen.com.br'
  
  return {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    '@id': `${siteUrl}/blog/${article.slug}`,
    headline: article.title,
    description: article.description || '',
    image: article.image ? (article.image.startsWith('http') ? article.image : `${siteUrl}${article.image}`) : undefined,
    datePublished: article.publishedAt,
    dateModified: article.updatedAt || article.publishedAt,
    author: {
      '@type': 'Organization',
      name: 'Agência Kaizen',
      url: siteUrl,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Agência Kaizen',
      logo: {
        '@type': 'ImageObject',
        url: `${siteUrl}/img/logos/logo-kaizen-maior.webp`,
      },
    },
  }
}

/**
 * Gera schema BreadcrumbList
 */
export function generateBreadcrumbSchema(items: Array<{ name: string; url?: string }>): BreadcrumbListSchema {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://site2025.agenciakaizen.com.br'
  
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url ? (item.url.startsWith('http') ? item.url : `${siteUrl}${item.url}`) : undefined,
    })),
  }
}



