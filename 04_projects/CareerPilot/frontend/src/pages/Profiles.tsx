import { useState } from 'react'
import { Plus, CheckCircle2, Circle, Pencil, X, Save, UserCircle2 } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useAsync } from '@/hooks/useAsync'
import { getProfiles, createProfile, updateProfile } from '@/lib/api'
import type { Profile } from '@/types'

const PRESETS = [
  { name: 'Data Engineer',       slug: 'data-engineer',        title: 'Senior Data Engineer',     skills: ['Python', 'Spark', 'Kafka', 'Airflow', 'dbt', 'PostgreSQL'], keywords: ['Data Pipeline', 'ETL', 'Delta Lake', 'BigQuery', 'Databricks'] },
  { name: 'Data Architect',      slug: 'data-architect',       title: 'Data Architect',            skills: ['Architecture', 'Data Modeling', 'Snowflake', 'dbt', 'Redshift'], keywords: ['Data Mesh', 'Data Lake', 'MDM', 'Lakehouse'] },
  { name: 'Azure Data Engineer', slug: 'azure-data-engineer',  title: 'Azure Data Engineer',       skills: ['ADF', 'Synapse', 'ADLS', 'Azure Databricks', 'Power BI'], keywords: ['Azure', 'ADF', 'Synapse Analytics', 'Data Factory'] },
  { name: 'Databricks Engineer', slug: 'databricks-engineer',  title: 'Databricks Engineer',       skills: ['Databricks', 'MLflow', 'Delta Live Tables', 'Spark', 'Unity Catalog'], keywords: ['Databricks', 'Lakehouse', 'MLflow', 'Delta Lake'] },
  { name: 'AI/ML Data Engineer', slug: 'aiml-data-engineer',   title: 'AI/ML Data Engineer',       skills: ['ML Pipelines', 'Kubeflow', 'Airflow', 'Python', 'TensorFlow'], keywords: ['ML Pipeline', 'Feature Store', 'MLOps', 'LLM'] },
]

function ProfileCard({ profile, onToggle, onEdit }: {
  profile: Profile
  onToggle: (id: string, active: boolean) => void
  onEdit: (p: Profile) => void
}) {
  return (
    <Card className={profile.is_active ? 'border-indigo-600/30' : 'opacity-60'}>
      <CardContent className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-chivo font-semibold text-base text-foreground">{profile.name}</h3>
              {profile.is_active
                ? <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                : <Circle className="w-4 h-4 text-muted-foreground" />}
            </div>
            <p className="text-xs text-muted-foreground mt-0.5">
              {profile.title}
              {profile.experience_years > 0 ? ` · ${profile.experience_years}y exp` : ''}
            </p>
          </div>
          <button
            onClick={() => onEdit(profile)}
            className="w-7 h-7 flex items-center justify-center rounded hover:bg-accent text-muted-foreground hover:text-foreground transition-colors"
          >
            <Pencil className="w-3.5 h-3.5" />
          </button>
        </div>

        {profile.summary && (
          <p className="text-xs text-muted-foreground mb-3 line-clamp-2">{profile.summary}</p>
        )}

        {/* Skills */}
        {profile.skills.length > 0 && (
          <div className="mb-3">
            <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1.5">Skills</p>
            <div className="flex flex-wrap gap-1">
              {profile.skills.map(s => (
                <span key={s} className="text-[10px] bg-secondary text-foreground px-2 py-0.5 rounded border border-border">{s}</span>
              ))}
            </div>
          </div>
        )}

        {/* Keywords */}
        {profile.keywords.length > 0 && (
          <div className="mb-3">
            <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1.5">ATS Keywords</p>
            <div className="flex flex-wrap gap-1">
              {profile.keywords.map(k => (
                <span key={k} className="text-[10px] bg-indigo-950/40 text-indigo-300 px-2 py-0.5 rounded border border-indigo-900/40">{k}</span>
              ))}
            </div>
          </div>
        )}

        {/* Locations */}
        {profile.preferred_locations.length > 0 && (
          <div className="mb-4">
            <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1.5">Locations</p>
            <div className="flex flex-wrap gap-1">
              {profile.preferred_locations.map(l => <Badge key={l} variant="outline" className="text-[10px]">{l}</Badge>)}
              {profile.remote_only && <Badge variant="info" className="text-[10px]">Remote Only</Badge>}
            </div>
          </div>
        )}

        {/* Toggle */}
        <div className="flex items-center justify-between pt-3 border-t border-border">
          <p className="text-[10px] text-muted-foreground">
            Created {new Date(profile.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
          </p>
          <Button
            size="sm"
            variant={profile.is_active ? 'outline' : 'default'}
            onClick={() => onToggle(profile.id, !profile.is_active)}
          >
            {profile.is_active ? 'Deactivate' : 'Activate'}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

interface ProfileFormProps {
  initial?: Partial<Profile>
  onSave: (data: {
    name: string; slug: string; title: string; summary: string
    skills: string[]; keywords: string[]; preferred_locations: string[]
    experience_years: number; remote_only: boolean
  }) => Promise<void>
  onCancel: () => void
}

function ProfileForm({ initial, onSave, onCancel }: ProfileFormProps) {
  const [name, setName]         = useState(initial?.name ?? '')
  const [title, setTitle]       = useState(initial?.title ?? '')
  const [summary, setSummary]   = useState(initial?.summary ?? '')
  const [skills, setSkills]     = useState((initial?.skills ?? []).join(', '))
  const [keywords, setKeywords] = useState((initial?.keywords ?? []).join(', '))
  const [locations, setLocations] = useState((initial?.preferred_locations ?? []).join(', '))
  const [years, setYears]       = useState(String(initial?.experience_years ?? 0))
  const [saving, setSaving]     = useState(false)
  const [error, setError]       = useState<string | null>(null)

  const handleSave = async () => {
    if (!name.trim() || !title.trim()) { setError('Name and title are required.'); return }
    setSaving(true)
    setError(null)
    try {
      await onSave({
        name: name.trim(),
        slug: name.trim().toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, ''),
        title: title.trim(),
        summary: summary.trim(),
        skills: skills.split(',').map(s => s.trim()).filter(Boolean),
        keywords: keywords.split(',').map(s => s.trim()).filter(Boolean),
        preferred_locations: locations.split(',').map(s => s.trim()).filter(Boolean),
        experience_years: parseInt(years) || 0,
        remote_only: false,
      })
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card className="border-indigo-600/30">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm">{initial ? 'Edit Profile' : 'New Profile'}</CardTitle>
          <button onClick={onCancel} className="text-muted-foreground hover:text-foreground"><X className="w-4 h-4" /></button>
        </div>
      </CardHeader>
      <CardContent className="pt-0 space-y-3">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <p className="text-xs text-muted-foreground mb-1">Profile Name *</p>
            <Input value={name} onChange={e => setName(e.target.value)} placeholder="Data Engineer" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-1">Job Title *</p>
            <Input value={title} onChange={e => setTitle(e.target.value)} placeholder="Senior Data Engineer" />
          </div>
        </div>
        <div>
          <p className="text-xs text-muted-foreground mb-1">Summary</p>
          <Input value={summary} onChange={e => setSummary(e.target.value)} placeholder="Brief professional summary…" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <p className="text-xs text-muted-foreground mb-1">Skills (comma separated)</p>
            <Input value={skills} onChange={e => setSkills(e.target.value)} placeholder="Python, Spark, Kafka" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-1">ATS Keywords</p>
            <Input value={keywords} onChange={e => setKeywords(e.target.value)} placeholder="Data Pipeline, ETL, Delta Lake" />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <p className="text-xs text-muted-foreground mb-1">Preferred Locations</p>
            <Input value={locations} onChange={e => setLocations(e.target.value)} placeholder="Bangalore, Remote" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-1">Experience (years)</p>
            <Input value={years} onChange={e => setYears(e.target.value)} type="number" min="0" max="30" />
          </div>
        </div>
        {error && <p className="text-xs text-red-400">{error}</p>}
        <div className="flex gap-2 pt-1">
          <Button size="sm" onClick={handleSave} disabled={saving}>
            <Save className="w-3.5 h-3.5" />{saving ? 'Saving…' : 'Save Profile'}
          </Button>
          <Button size="sm" variant="outline" onClick={onCancel}>Cancel</Button>
        </div>
      </CardContent>
    </Card>
  )
}

export default function Profiles() {
  const [showPresets, setShowPresets]   = useState(false)
  const [showNewForm, setShowNewForm]   = useState(false)
  const [editProfile, setEditProfile]   = useState<Profile | null>(null)
  const [savingPreset, setSavingPreset] = useState<string | null>(null)

  const { data, loading, error, reload } = useAsync<Profile[]>(getProfiles)
  const profiles = data ?? []

  const handleToggle = async (id: string, active: boolean) => {
    await updateProfile(id, { is_active: active } as Partial<Profile>)
    reload()
  }

  const handleCreate = async (formData: Parameters<typeof createProfile>[0]) => {
    await createProfile(formData)
    reload()
    setShowNewForm(false)
  }

  const handleUpdate = async (formData: Parameters<typeof createProfile>[0]) => {
    if (!editProfile) return
    await updateProfile(editProfile.id, formData as Partial<Profile>)
    reload()
    setEditProfile(null)
  }

  const addPreset = async (preset: typeof PRESETS[0]) => {
    const exists = profiles.some(p => p.slug === preset.slug)
    if (exists) return
    setSavingPreset(preset.slug)
    try {
      await createProfile({
        name: preset.name,
        slug: preset.slug,
        title: preset.title,
        summary: `Experienced ${preset.title} with expertise in ${preset.skills.slice(0, 3).join(', ')}.`,
        skills: preset.skills,
        keywords: preset.keywords,
        preferred_locations: ['Bangalore', 'Remote'],
        experience_years: 5,
        remote_only: false,
      })
      reload()
    } finally {
      setSavingPreset(null)
    }
  }

  return (
    <div className="p-6 space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-chivo text-xl font-semibold text-foreground">Profiles</h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            {loading ? 'Loading…' : `${profiles.filter(p => p.is_active).length} active · ${profiles.length} total`}
          </p>
        </div>
        <div className="flex gap-2">
          <Button size="sm" variant="outline" onClick={() => { setShowPresets(!showPresets); setShowNewForm(false) }}>
            <Plus className="w-3.5 h-3.5" />Quick Add
          </Button>
          <Button size="sm" onClick={() => { setShowNewForm(!showNewForm); setShowPresets(false); setEditProfile(null) }}>
            <Plus className="w-3.5 h-3.5" />New Profile
          </Button>
        </div>
      </div>

      {error && (
        <div className="text-xs text-red-400 bg-red-950/20 border border-red-900/30 rounded-md px-4 py-3">
          Error loading profiles: {error}
        </div>
      )}

      {/* Preset picker */}
      {showPresets && (
        <Card className="border-indigo-600/30">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm">Quick Add Preset</CardTitle>
              <button onClick={() => setShowPresets(false)} className="text-muted-foreground hover:text-foreground"><X className="w-4 h-4" /></button>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="grid grid-cols-5 gap-2">
              {PRESETS.map(preset => {
                const exists = profiles.some(p => p.slug === preset.slug)
                const isSaving = savingPreset === preset.slug
                return (
                  <button
                    key={preset.slug}
                    onClick={() => addPreset(preset)}
                    disabled={exists || isSaving}
                    className={`p-3 rounded-md border text-left transition-colors ${
                      exists ? 'border-border bg-secondary/30 opacity-50 cursor-not-allowed' :
                      isSaving ? 'border-indigo-600/50 bg-indigo-950/20 cursor-wait' :
                      'border-border hover:border-indigo-600/50 hover:bg-indigo-950/20'
                    }`}
                  >
                    <p className="text-xs font-medium text-foreground">{preset.name}</p>
                    <p className="text-[10px] text-muted-foreground mt-1">{preset.skills.slice(0, 2).join(', ')}</p>
                    {exists && <p className="text-[10px] text-emerald-400 mt-1">Added</p>}
                    {isSaving && <p className="text-[10px] text-indigo-400 mt-1">Saving…</p>}
                  </button>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* New profile form */}
      {showNewForm && !editProfile && (
        <ProfileForm onSave={handleCreate} onCancel={() => setShowNewForm(false)} />
      )}

      {/* Edit form */}
      {editProfile && (
        <ProfileForm initial={editProfile} onSave={handleUpdate} onCancel={() => setEditProfile(null)} />
      )}

      {/* Profile grid */}
      {loading ? (
        <div className="grid grid-cols-2 gap-4">
          {[1, 2].map(i => <div key={i} className="h-64 rounded-lg bg-card border border-border animate-pulse" />)}
        </div>
      ) : profiles.length === 0 ? (
        <div className="py-16 text-center">
          <UserCircle2 className="w-10 h-10 mx-auto mb-3 text-muted-foreground opacity-30" />
          <p className="text-sm text-foreground mb-1">No profiles yet</p>
          <p className="text-xs text-muted-foreground mb-4">Add a preset or create a custom profile to start job discovery.</p>
          <Button size="sm" onClick={() => setShowPresets(true)}>
            <Plus className="w-3.5 h-3.5" />Quick Add Preset
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {profiles.map(profile => (
            editProfile?.id === profile.id ? null : (
              <ProfileCard key={profile.id} profile={profile} onToggle={handleToggle} onEdit={setEditProfile} />
            )
          ))}
          {/* Empty slot */}
          {!showNewForm && !editProfile && (
            <button
              onClick={() => setShowNewForm(true)}
              className="rounded-lg border border-dashed border-border hover:border-indigo-600/50 flex flex-col items-center justify-center gap-2 py-12 transition-colors group min-h-[180px]"
            >
              <div className="w-8 h-8 rounded-full border border-border group-hover:border-indigo-600/50 flex items-center justify-center">
                <Plus className="w-4 h-4 text-muted-foreground group-hover:text-indigo-400" />
              </div>
              <p className="text-sm text-muted-foreground group-hover:text-foreground">Add Profile</p>
            </button>
          )}
        </div>
      )}
    </div>
  )
}
