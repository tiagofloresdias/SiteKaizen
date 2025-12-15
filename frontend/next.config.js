/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Images
  images: {
    domains: ['site2025.agenciakaizen.com.br', 'www.agenciakaizen.com.br'],
    formats: ['image/webp', 'image/avif'],
  },
  
  // Headers para SEO
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ]
  },
  
  // Variáveis de ambiente
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://site2025.agenciakaizen.com.br/api/v1',
    NEXT_PUBLIC_SITE_URL: process.env.NEXT_PUBLIC_SITE_URL || 'https://site2025.agenciakaizen.com.br',
  },
  
  // Otimizações para produção
  compress: true,
  poweredByHeader: false,
  
  // Output standalone para melhor performance na Vercel
  output: 'standalone',
}

module.exports = nextConfig



