import Link from 'next/link'
import { generateBreadcrumbSchema } from './JsonLd'

export interface BreadcrumbItem {
  name: string
  url?: string
}

export interface BreadcrumbProps {
  items: BreadcrumbItem[]
  showJsonLd?: boolean
}

export default function Breadcrumb({ items, showJsonLd = true }: BreadcrumbProps) {
  const schema = showJsonLd ? generateBreadcrumbSchema(items) : null

  return (
    <>
      {schema && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
      )}
      
      <nav aria-label="Breadcrumb" className="mb-8">
        <ol className="flex items-center space-x-2 text-sm text-text-muted">
          {items.map((item, index) => (
            <li key={index} className="flex items-center">
              {index > 0 && (
                <span className="mx-2 text-text-muted" aria-hidden="true">
                  /
                </span>
              )}
              {item.url ? (
                <Link
                  href={item.url}
                  className="hover:text-primary transition-colors"
                >
                  {item.name}
                </Link>
              ) : (
                <span className="text-text" aria-current="page">
                  {item.name}
                </span>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  )
}



