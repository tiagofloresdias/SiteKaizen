'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Image from 'next/image'
import Button from '@/components/ui/Button'
import { Company } from '@/lib/api'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://site2025.agenciakaizen.com.br/api/v1'

export default function AdminEmpresasPage() {
  const router = useRouter()
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [editingCompany, setEditingCompany] = useState<Company | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    tagline: '',
    description: '',
    logo_url: '',
    website_url: '',
    contact_email: '',
    phone: '',
    is_active: true,
    order: 0,
    meta_description: '',
    category_id: '',
  })
  const [categories, setCategories] = useState<any[]>([])

  useEffect(() => {
    // Verificar token
    const storedToken = localStorage.getItem('token')
    if (!storedToken) {
      router.push('/admin/login')
      return
    }
    setToken(storedToken)
    loadCompanies(storedToken)
    loadCategories(storedToken)
  }, [router])

  const loadCompanies = async (authToken: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/companies?limit=100`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      })
      if (response.ok) {
        const data = await response.json()
        setCompanies(data.data || [])
      }
    } catch (error) {
      console.error('Erro ao carregar empresas:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadCategories = async (authToken: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/company-categories`, {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      })
      if (response.ok) {
        const data = await response.json()
        setCategories(data || [])
        if (data.length > 0 && !formData.category_id) {
          setFormData(prev => ({ ...prev, category_id: data[0].id }))
        }
      }
    } catch (error) {
      console.error('Erro ao carregar categorias:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!token) return

    try {
      const url = editingCompany
        ? `${API_BASE_URL}/companies/${editingCompany.id}`
        : `${API_BASE_URL}/companies`
      
      const method = editingCompany ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        await loadCompanies(token)
        resetForm()
        alert(editingCompany ? 'Empresa atualizada com sucesso!' : 'Empresa criada com sucesso!')
      } else {
        const error = await response.json()
        alert(`Erro: ${error.detail || 'Erro ao salvar empresa'}`)
      }
    } catch (error) {
      console.error('Erro ao salvar empresa:', error)
      alert('Erro ao salvar empresa')
    }
  }

  const handleDelete = async (companyId: string) => {
    if (!token || !confirm('Tem certeza que deseja deletar esta empresa?')) return

    try {
      const response = await fetch(`${API_BASE_URL}/companies/${companyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (response.ok) {
        await loadCompanies(token)
        alert('Empresa deletada com sucesso!')
      } else {
        alert('Erro ao deletar empresa')
      }
    } catch (error) {
      console.error('Erro ao deletar empresa:', error)
      alert('Erro ao deletar empresa')
    }
  }

  const handleEdit = (company: Company) => {
    setEditingCompany(company)
    setFormData({
      name: company.name,
      slug: company.slug,
      tagline: company.tagline || '',
      description: company.description || '',
      logo_url: company.logo_url || '',
      website_url: company.website_url || '',
      contact_email: company.contact_email || '',
      phone: company.phone || '',
      is_active: company.is_active,
      order: company.order || 0,
      meta_description: company.meta_description || '',
      category_id: company.category?.id || '',
    })
    setShowForm(true)
  }

  const resetForm = () => {
    setFormData({
      name: '',
      slug: '',
      tagline: '',
      description: '',
      logo_url: '',
      website_url: '',
      contact_email: '',
      phone: '',
      is_active: true,
      order: 0,
      meta_description: '',
      category_id: categories[0]?.id || '',
    })
    setEditingCompany(null)
    setShowForm(false)
  }

  const generateSlug = (name: string) => {
    return name
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <p>Carregando...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white pt-20">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold">Gerenciar Empresas</h1>
          <Button onClick={() => resetForm()}>
            {showForm ? 'Cancelar' : '+ Nova Empresa'}
          </Button>
        </div>

        {showForm && (
          <div className="mb-8 ka-card p-6">
            <h2 className="text-2xl font-bold mb-6">
              {editingCompany ? 'Editar Empresa' : 'Nova Empresa'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Nome *</label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => {
                      setFormData({ ...formData, name: e.target.value })
                      if (!editingCompany) {
                        setFormData(prev => ({ ...prev, slug: generateSlug(e.target.value) }))
                      }
                    }}
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Slug *</label>
                  <input
                    type="text"
                    required
                    value={formData.slug}
                    onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Tagline</label>
                  <input
                    type="text"
                    value={formData.tagline}
                    onChange={(e) => setFormData({ ...formData, tagline: e.target.value })}
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Categoria *</label>
                  <select
                    required
                    value={formData.category_id}
                    onChange={(e) => setFormData({ ...formData, category_id: e.target.value })}
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  >
                    <option value="">Selecione...</option>
                    {categories.map(cat => (
                      <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Logo URL</label>
                  <input
                    type="url"
                    value={formData.logo_url}
                    onChange={(e) => setFormData({ ...formData, logo_url: e.target.value })}
                    placeholder="/img/logo-empresa.webp"
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Website URL</label>
                  <input
                    type="url"
                    value={formData.website_url}
                    onChange={(e) => setFormData({ ...formData, website_url: e.target.value })}
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Email de Contato</label>
                  <input
                    type="email"
                    value={formData.contact_email}
                    onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Telefone</label>
                  <input
                    type="text"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Ordem</label>
                  <input
                    type="number"
                    value={formData.order}
                    onChange={(e) => setFormData({ ...formData, order: parseInt(e.target.value) || 0 })}
                    className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                  />
                </div>
                <div className="flex items-center">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.is_active}
                      onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                      className="mr-2"
                    />
                    <span>Ativa</span>
                  </label>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Descrição</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={4}
                  className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Meta Description (SEO)</label>
                <input
                  type="text"
                  maxLength={160}
                  value={formData.meta_description}
                  onChange={(e) => setFormData({ ...formData, meta_description: e.target.value })}
                  className="w-full px-4 py-2 bg-dark-3 border border-ka-border rounded-lg text-white"
                />
              </div>
              <div className="flex gap-4">
                <Button type="submit" variant="primary">
                  {editingCompany ? 'Atualizar' : 'Criar'} Empresa
                </Button>
                <Button type="button" variant="outline" onClick={resetForm}>
                  Cancelar
                </Button>
              </div>
            </form>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {companies.map((company) => (
            <div key={company.id} className="ka-card p-6">
              {company.logo_url && (
                <div className="mb-4 h-16 flex items-center">
                  <Image
                    src={company.logo_url}
                    alt={company.name}
                    width={200}
                    height={80}
                    className="max-h-16 w-auto object-contain"
                  />
                </div>
              )}
              <h3 className="text-xl font-bold mb-2">{company.name}</h3>
              {company.tagline && (
                <p className="text-primary text-sm mb-2">{company.tagline}</p>
              )}
              <div className="flex gap-2 mt-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleEdit(company)}
                >
                  Editar
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDelete(company.id)}
                >
                  Deletar
                </Button>
              </div>
            </div>
          ))}
        </div>

        {companies.length === 0 && !showForm && (
          <div className="text-center py-20">
            <p className="text-text-muted">Nenhuma empresa cadastrada.</p>
          </div>
        )}
      </div>
    </div>
  )
}

