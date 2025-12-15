/**
 * Componente SEO para Next.js App Router
 * No App Router, os metadados são definidos via Metadata API ou exportando metadata
 * Este componente é útil apenas para JSON-LD dinâmico
 */

export interface SeoProps {
  jsonLd?: object | object[]
}

export default function Seo({ jsonLd }: SeoProps) {
  if (!jsonLd) return null

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(Array.isArray(jsonLd) ? jsonLd : [jsonLd]),
      }}
    />
  )
}

