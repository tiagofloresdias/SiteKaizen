import { Metadata } from 'next'
import { getLocations, Location } from '@/lib/api'
import Breadcrumb from '@/components/seo/Breadcrumb'
import { generateOrganizationSchema, generateLocalBusinessSchema } from '@/components/seo/JsonLd'

export const metadata: Metadata = {
  title: 'Onde Estamos',
  description: 'Estamos nas principais regiões do Brasil levando estratégias de alto performance para empresas que querem acelerar.',
}

export default async function OndeEstamosPage() {
  let locations: Location[] = []
  try {
    const locationsResponse = await getLocations({ is_active: true })
    locations = locationsResponse.data || []
  } catch (error) {
    console.warn('Erro ao buscar localizações:', error)
    locations = []
  }

  const breadcrumbItems = [
    { name: 'Home', url: '/' },
    { name: 'Onde Estamos', url: '/onde-estamos' },
  ]

  // JSON-LD
  const organizationSchema = generateOrganizationSchema()
  const localBusinessSchemas = locations.map((location) =>
    generateLocalBusinessSchema({
      name: location.name,
      city: location.city,
      state: location.state,
      address: location.address,
      postal_code: location.postal_code,
      country: location.country,
      phone: location.phone,
      email: location.email,
      latitude: location.latitude ? Number(location.latitude) : undefined,
      longitude: location.longitude ? Number(location.longitude) : undefined,
      opening_hours: location.opening_hours,
    })
  )
  const schemas = [organizationSchema, ...localBusinessSchemas]

  return (
    <>
      {/* JSON-LD */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(schemas) }}
      />

      <div className="pt-20 min-h-screen bg-black">
        {/* Hero Section */}
        <section className="py-16 border-b border-ka-border">
          <div className="container mx-auto px-4">
            <Breadcrumb items={breadcrumbItems} />
            <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
              Presença forte. Crescimento sem limites.
            </h1>
            <p className="text-lg text-text-muted max-w-3xl">
              Estamos nas principais regiões do Brasil levando estratégias de alto performance para empresas que 
              querem acelerar. Desde que você esteja, a Kaizen está pronta para impulsionar seu negócio.
            </p>
          </div>
        </section>

        {/* Locations Grid */}
        <section className="py-16">
          <div className="container mx-auto px-4">
            {locations.length === 0 ? (
              <div className="text-center py-20">
                <p className="text-text-muted text-lg">
                  Nenhuma localização cadastrada no momento.
                </p>
              </div>
            ) : (
              <>
                <h2 className="text-3xl font-bold text-white mb-8 text-center">
                  Se sua meta é crescer, nós estamos por perto.
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {locations.map((location) => (
                    <div key={location.id} className="ka-card p-6">
                      <div className="flex items-center mb-4">
                        <div className="w-14 h-14 rounded-full bg-gradient-to-r from-primary to-primary-light flex items-center justify-center text-white text-xl mr-4">
                          📍
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-white">{location.name}</h3>
                          <p className="text-text-muted">{location.city}, {location.state}</p>
                        </div>
                      </div>
                      
                      <div className="text-text-muted mb-4">
                        <p className="mb-2">{location.address}</p>
                        {location.postal_code && (
                          <p className="mb-2">CEP: {location.postal_code}</p>
                        )}
                        {location.opening_hours && (
                          <p className="mb-2">⏰ {location.opening_hours}</p>
                        )}
                      </div>

                      <div className="space-y-2">
                        {location.phone && (
                          <a
                            href={`tel:${location.phone.replace(/\D/g, '')}`}
                            className="block text-primary hover:underline"
                          >
                            📞 {location.phone}
                          </a>
                        )}
                        {location.email && (
                          <a
                            href={`mailto:${location.email}`}
                            className="block text-primary hover:underline"
                          >
                            ✉️ {location.email}
                          </a>
                        )}
                        {location.maps_url && (
                          <a
                            href={location.maps_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="block text-primary hover:underline"
                          >
                            🗺️ Ver no Google Maps
                          </a>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 bg-gradient-to-r from-primary/10 to-primary-light/10">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Entre em contato
            </h2>
            <p className="text-lg text-text-muted mb-8 max-w-2xl mx-auto">
              Preencha o formulário e fale com nosso time.
            </p>
            <a href="/contato" className="btn-primary text-lg px-8 py-4">
              Fale Conosco
            </a>
          </div>
        </section>
      </div>
    </>
  )
}

