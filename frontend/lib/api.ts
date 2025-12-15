/**
 * Cliente API FastAPI - Integração com backend PostgreSQL
 * 
 * IMPORTANTE: Na Vercel, a API será acessada via URL de produção
 * Não há conflito de portas pois a Vercel gerencia isso automaticamente
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://site2025.agenciakaizen.com.br/api/v1'

export interface Company {
  id: string
  name: string
  slug: string
  tagline?: string
  description?: string
  logo_url?: string
  featured_image_url?: string
  website_url?: string
  contact_email?: string
  phone?: string
  is_active: boolean
  order: number
  meta_description?: string
  founded_date?: string
  category: {
    id: string
    name: string
    slug: string
    color: string
  }
  features: Array<{
    id: string
    title: string
    description: string
    icon?: string
    order: number
  }>
  created_at: string
  updated_at?: string
}

export interface Article {
  id: string
  title: string
  slug: string
  excerpt?: string
  content: string
  cover_image_url?: string
  social_image_url?: string
  is_featured: boolean
  is_published: boolean
  reading_time: number
  seo_title?: string
  seo_description?: string
  meta_keywords?: string
  category?: {
    id: string
    name: string
    slug: string
  }
  published_at?: string
  created_at: string
  updated_at?: string
}

export interface Location {
  id: string
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
  maps_url?: string
  place_id?: string
  opening_hours?: string
  is_main_office: boolean
  is_active: boolean
  order: number
  created_at: string
  updated_at?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  pages: number
}

export interface ListParams {
  page?: number
  limit?: number
  category?: string
  is_active?: boolean
  is_featured?: boolean
  is_published?: boolean
}

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      next: { revalidate: 3600 }, // ISR: revalidar a cada 1h
      // Timeout para build
      signal: AbortSignal.timeout(5000), // 5 segundos timeout
    })
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`)
    }
    
    return response.json()
  } catch (error: any) {
    // Durante build, retornar dados vazios se API não estiver disponível
    if (error.code === 'ECONNREFUSED' || error.name === 'AbortError') {
      console.warn(`API não disponível em ${url}, retornando dados vazios para build`)
      return { data: [], total: 0, page: 1, limit: 20, pages: 0 } as T
    }
    throw error
  }
}

/**
 * Companies
 */
export async function getCompanies(params?: ListParams): Promise<PaginatedResponse<Company>> {
  const searchParams = new URLSearchParams()
  if (params?.page) searchParams.append('page', params.page.toString())
  if (params?.limit) searchParams.append('limit', params.limit.toString())
  if (params?.category) searchParams.append('category', params.category)
  if (params?.is_active !== undefined) searchParams.append('is_active', params.is_active.toString())
  
  const query = searchParams.toString()
  return fetchAPI<PaginatedResponse<Company>>(`/companies${query ? `?${query}` : ''}`)
}

export async function getCompanyBySlug(slug: string): Promise<Company> {
  return fetchAPI<Company>(`/companies/${slug}`)
}

/**
 * Articles
 */
export async function getArticles(params?: ListParams): Promise<PaginatedResponse<Article>> {
  const searchParams = new URLSearchParams()
  if (params?.page) searchParams.append('page', params.page.toString())
  if (params?.limit) searchParams.append('limit', params.limit.toString())
  if (params?.category) searchParams.append('category', params.category)
  if (params?.is_featured !== undefined) searchParams.append('is_featured', params.is_featured.toString())
  if (params?.is_published !== undefined) searchParams.append('is_published', params.is_published.toString())
  
  const query = searchParams.toString()
  return fetchAPI<PaginatedResponse<Article>>(`/articles${query ? `?${query}` : ''}`)
}

export async function getArticleBySlug(slug: string): Promise<Article> {
  return fetchAPI<Article>(`/articles/${slug}`)
}

/**
 * Locations
 */
export async function getLocations(params?: {
  is_active?: boolean
  is_main_office?: boolean
}): Promise<{ data: Location[]; total: number }> {
  const searchParams = new URLSearchParams()
  if (params?.is_active !== undefined) searchParams.append('is_active', params.is_active.toString())
  if (params?.is_main_office !== undefined) searchParams.append('is_main_office', params.is_main_office.toString())
  
  const query = searchParams.toString()
  return fetchAPI<{ data: Location[]; total: number }>(`/locations${query ? `?${query}` : ''}`)
}

/**
 * Sitemap Data
 */
export async function getSitemapData(): Promise<{
  companies: string[]
  articles: string[]
  static_pages: string[]
}> {
  return fetchAPI<{
    companies: string[]
    articles: string[]
    static_pages: string[]
  }>('/sitemap-data')
}

