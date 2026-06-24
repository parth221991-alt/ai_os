import { useState } from 'react'
import { Search, ExternalLink, Zap, Wifi, RefreshCw, Briefcase } from 'lucide-react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import { useAsync } from '@/hooks/useAsync'
import { getJobs, getProfiles, triggerDiscovery } from '@/lib/api'
import type { Job, Profile } from '@/types'

const PLATFORM_COLORS: Record<string, string> = {
  linkedin: 'text-sky-400 border-sky-900/40 bg-sky-950/40',
  naukri:   'text-orange-400 border-orange-900/40 bg-orange-950/40',
  indeed:   'text-blue-400 border-blue-900/40 bg-blue-950/40',
  company:  'text-purple-400 border-purple-900/40 bg-purple-950/40',
}
const PLATFORM_LABEL: Record<string, string> = {
  linkedin: 'LinkedIn', naukri: 'Naukri', indeed: 'Indeed', company: 'Company',
}

function ScorePill({ score }: { score: number }) {
  const color = score >= 85 ? 'text-emerald-400' : score >= 70 ? 'text-amber-400' : 'text-muted-foreground'
  return (
    <div className="flex flex-col items-end gap-1 w-14">
      <span className={`font-mono text-sm font-semibold ${color}`}>{Math.round(score)}%</span>
      <Progress value={score} className="h-1 w-full" />
    </div>
  )
}

function EmptyJobs({ onDiscover }: { onDiscover: () => void }) {
  return (
    <div className="py-16 text-center">
      <Briefcase className="w-10 h-10 mx-auto mb-3 text-muted-foreground opacity-30" />
      <p className="text-sm text-foreground mb-1">No jobs discovered yet</p>
      <p className="text-xs text-muted-foreground mb-4">Run discovery to start scraping LinkedIn, Naukri, and Indeed.</p>
      <Button size="sm" onClick={onDiscover}>Run Discovery Now</Button>
    </div>
  )
}

export default function Jobs() {
  const [search, setSearch]       = useState('')
  const [platform, setPlatform]   = useState('all')
  const [minScore, setMinScore]   = useState('0')
  const [profileId, setProfileId] = useState('all')
  const [tab, setTab]             = useState('all')
  const [discovering, setDisc]    = useState(false)

  const profiles = useAsync<Profile[]>(getProfiles)
  const jobs = useAsync<Job[]>(
    () => getJobs({
      platform: platform !== 'all' ? platform : undefined,
      min_score: parseInt(minScore) || 0,
      profile_id: profileId !== 'all' ? profileId : undefined,
      limit: 100,
    }),
    [platform, minScore, profileId]
  )

  const handleDiscover = async () => {
    setDisc(true)
    try { await triggerDiscovery() } catch (_) { /* */ }
    setTimeout(() => { setDisc(false); jobs.reload() }, 3000)
  }

  const jobList = jobs.data ?? []

  const filtered = jobList.filter(j => {
    const matchSearch = !search ||
      j.title.toLowerCase().includes(search.toLowerCase()) ||
      j.company.toLowerCase().includes(search.toLowerCase())
    const matchTab =
      tab === 'all' ? true :
      tab === 'easy' ? j.is_easy_apply :
      tab === 'remote' ? j.is_remote : true
    return matchSearch && matchTab
  })

  const easyCount   = jobList.filter(j => j.is_easy_apply).length
  const remoteCount = jobList.filter(j => j.is_remote).length

  return (
    <div className="p-6 space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-chivo text-xl font-semibold text-foreground">Jobs</h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            {jobs.loading ? 'Loading…' : `${jobList.length} jobs in database`}
          </p>
        </div>
        <Button size="sm" onClick={handleDiscover} disabled={discovering}>
          {discovering ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Zap className="w-3.5 h-3.5" />}
          {discovering ? 'Running…' : 'Discover'}
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
              <Input
                placeholder="Search title or company…"
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="pl-9"
              />
            </div>
            <Select value={platform} onValueChange={v => { setPlatform(v); }}>
              <SelectTrigger className="w-36"><SelectValue placeholder="Platform" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Platforms</SelectItem>
                <SelectItem value="linkedin">LinkedIn</SelectItem>
                <SelectItem value="naukri">Naukri</SelectItem>
                <SelectItem value="indeed">Indeed</SelectItem>
                <SelectItem value="company">Company</SelectItem>
              </SelectContent>
            </Select>
            <Select value={minScore} onValueChange={v => { setMinScore(v); }}>
              <SelectTrigger className="w-32"><SelectValue placeholder="Min Score" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="0">Any Score</SelectItem>
                <SelectItem value="60">60%+</SelectItem>
                <SelectItem value="70">70%+</SelectItem>
                <SelectItem value="80">80%+</SelectItem>
                <SelectItem value="90">90%+</SelectItem>
              </SelectContent>
            </Select>
            <Select value={profileId} onValueChange={v => { setProfileId(v); }}>
              <SelectTrigger className="w-44"><SelectValue placeholder="Profile" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Profiles</SelectItem>
                {(profiles.data ?? []).map(p => (
                  <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <CardHeader className="pb-0 px-5 pt-4">
          <Tabs value={tab} onValueChange={setTab}>
            <TabsList>
              <TabsTrigger value="all">All ({jobList.length})</TabsTrigger>
              <TabsTrigger value="easy">
                <Zap className="w-3 h-3 mr-1" />Easy Apply ({easyCount})
              </TabsTrigger>
              <TabsTrigger value="remote">
                <Wifi className="w-3 h-3 mr-1" />Remote ({remoteCount})
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </CardHeader>
        <CardContent className="p-0 pt-3">
          {jobs.error && (
            <div className="px-5 py-3 text-xs text-red-400 bg-red-950/20 border-b border-red-900/30">
              Error loading jobs: {jobs.error}
            </div>
          )}

          <div className="grid grid-cols-[2fr_1fr_1fr_1fr_auto] gap-3 px-5 py-2 border-b border-border text-[10px] text-muted-foreground uppercase tracking-wider font-medium">
            <span>Role</span><span>Platform</span><span>Location</span><span>Discovered</span><span className="text-right">Match</span>
          </div>

          <div className="divide-y divide-border/40">
            {jobs.loading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="px-5 py-4 flex gap-3">
                  <div className="flex-1 space-y-2">
                    <div className="h-4 w-48 rounded bg-secondary animate-pulse" />
                    <div className="h-3 w-32 rounded bg-secondary animate-pulse" />
                  </div>
                </div>
              ))
            ) : filtered.length === 0 ? (
              <EmptyJobs onDiscover={handleDiscover} />
            ) : filtered.map(job => (
              <div key={job.id} className="grid grid-cols-[2fr_1fr_1fr_1fr_auto] gap-3 px-5 py-3 items-center hover:bg-accent/20 transition-colors">
                {/* Role */}
                <div className="min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <p className="text-sm text-foreground font-medium truncate">{job.title}</p>
                    {job.is_easy_apply && (
                      <Badge variant="success" className="text-[10px] py-0 px-1.5 gap-1 shrink-0">
                        <Zap className="w-2.5 h-2.5" />Easy
                      </Badge>
                    )}
                    {job.is_remote && (
                      <Badge variant="info" className="text-[10px] py-0 px-1.5 gap-1 shrink-0">
                        <Wifi className="w-2.5 h-2.5" />Remote
                      </Badge>
                    )}
                  </div>
                  <p className="text-xs text-muted-foreground mt-0.5">{job.company}</p>
                  {(job.matched_keywords ?? []).length > 0 && (
                    <div className="flex gap-1 mt-1 flex-wrap">
                      {(job.matched_keywords ?? []).slice(0, 4).map(kw => (
                        <span key={kw} className="text-[10px] bg-indigo-950/40 text-indigo-300 px-1.5 py-0.5 rounded border border-indigo-900/30">{kw}</span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Platform */}
                <span className={`inline-flex text-[10px] px-2 py-0.5 rounded-full border font-medium w-fit ${PLATFORM_COLORS[job.platform] ?? ''}`}>
                  {PLATFORM_LABEL[job.platform] ?? job.platform}
                </span>

                {/* Location */}
                <p className="text-xs text-muted-foreground truncate">{job.location ?? '—'}</p>

                {/* Discovered */}
                <p className="text-xs text-muted-foreground font-mono">
                  {job.discovered_at ? new Date(job.discovered_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) : '—'}
                </p>

                {/* Score + Link */}
                <div className="flex items-center gap-3">
                  {job.match_score != null
                    ? <ScorePill score={job.match_score} />
                    : <span className="text-xs text-muted-foreground w-14 text-right">—</span>}
                  <a href={job.url} target="_blank" rel="noreferrer"
                    className="text-muted-foreground hover:text-foreground transition-colors">
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
