import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'
import { getCompanyBySlug, getCompanies } from '@/lib/api'
import Breadcrumb from '@/components/seo/Breadcrumb'
import { generateOrganizationSchema, generateLocalBusinessSchema } from '@/components/seo/JsonLd'

interface PageProps {
  params: {
    slug: string
  }
}

export async function generateStaticParams() {
  try {
    const companies = await getCompanies({ is_active: true, limit: 100 })
    return companies.data.map((company) => ({
      slug: company.slug,
    }))
  } catch (error) {
    // Durante build, se API não estiver disponível, retornar array vazio
    console.warn('API não disponível durante build, usando rotas dinâmicas')
    return []
  }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  try {
    const company = await getCompanyBySlug(params.slug)
    return {
      title: company.name,
      description: company.meta_description || company.tagline || `${company.name} - ${company.tagline}`,
      openGraph: {
        title: company.name,
        description: company.meta_description || company.tagline,
        images: company.featured_image_url ? [company.featured_image_url] : undefined,
      },
    }
  } catch {
    return {
      title: 'Empresa não encontrada',
    }
  }
}

export default async function CompanyDetailPage({ params }: PageProps) {
  let company
  try {
    company = await getCompanyBySlug(params.slug)
  } catch {
    notFound()
  }

  const breadcrumbItems = [
    { name: 'Home', url: '/' },
    { name: 'Nossas Empresas', url: '/nossas-empresas' },
    { name: company.name },
  ]

  // JSON-LD
  const organizationSchema = generateOrganizationSchema()
  const schemas = [organizationSchema]

  return (
    <>
      {/* JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schemas) }}
      />

      <div className="pt-20 min-h-screen bg-black">
        {/* Hero */}
        <section className="py-16 border-b border-ka-border">
          <div className="container mx-auto px-4">
            <Breadcrumb items={breadcrumbItems} />
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div>
                {company.logo_url && (
                  <Image
                    src={company.logo_url}
                    alt={company.name}
                    width={300}
                    height={120}
                    className="mb-6 h-20 w-auto object-contain"
                  />
                )}
                <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
                  {company.name}
                </h1>
                {company.tagline && (
                  <p className="text-2xl text-primary font-bold mb-6">{company.tagline}</p>
                )}
                {company.description && (
                  <div
                    className="text-lg text-text-muted leading-relaxed mb-6"
                    dangerouslySetInnerHTML={{ __html: company.description }}
                  />
                )}
                
                {company.category && (
                  <div className="mb-6">
                    <span
                      className="inline-block px-4 py-2 rounded-full text-sm font-medium text-white"
                      style={{ backgroundColor: company.category.color }}
                    >
                      {company.category.name}
                    </span>
                  </div>
                )}

                {(company.website_url || company.contact_email || company.phone) && (
                  <div className="flex flex-wrap gap-4">
                    {company.website_url && (
                      <a
                        href={company.website_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-primary"
                      >
                        Visitar Site
                      </a>
                    )}
                    {company.contact_email && (
                      <a href={`mailto:${company.contact_email}`} className="btn-outline">
                        Entrar em Contato
                      </a>
                    )}
                  </div>
                )}
              </div>

              {company.featured_image_url && (
                <div>
                  <Image
                    src={company.featured_image_url}
                    alt={company.name}
                    width={600}
                    height={400}
                    className="rounded-2xl w-full h-auto"
                  />
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Features */}
        {company.features && company.features.length > 0 && (
          <section className="py-16">
            <div className="container mx-auto px-4">
              <h2 className="text-3xl font-bold text-white mb-8">Características</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {company.features.map((feature) => (
                  <div key={feature.id} className="ka-card p-6">
                    {feature.icon && (
                      <div className="text-3xl text-primary mb-4">{feature.icon}</div>
                    )}
                    <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                    <p className="text-text-muted">{feature.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        {/* CTA */}
        <section className="py-16 bg-gradient-to-r from-primary/10 to-primary-light/10">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Interessado em saber mais?
            </h2>
            <p className="text-lg text-text-muted mb-8 max-w-2xl mx-auto">
              Entre em contato e descubra como podemos ajudar seu negócio.
            </p>
            <Link href="/contato" className="btn-primary text-lg px-8 py-4">
              Fale Conosco
            </Link>
          </div>
        </section>
      </div>
    </>
  )
}

