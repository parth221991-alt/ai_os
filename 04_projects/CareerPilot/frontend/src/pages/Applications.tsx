import { useState } from 'react'
import { Clock, CheckCircle2, XCircle, Calendar, Trophy, ArchiveX, ClipboardList } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Progress } from '@/components/ui/progress'
import { useAsync } from '@/hooks/useAsync'
import { getApplications, getPipeline, updateApplicationStatus } from '@/lib/api'
import type { Application, JobStatus, PipelineCount } from '@/types'

type Status = JobStatus

const STATUS_CONFIG: Record<string, {
  label: string
  color: string
  icon: React.FC<{ className?: string }>
  variant: 'default' | 'success' | 'destructive' | 'warning' | 'outline' | 'secondary' | 'info'
}> = {
  applied:         { label: 'Applied',         color: 'text-indigo-400',  icon: Clock,         variant: 'default' },
  interviewing:    { label: 'Interviewing',     color: 'text-emerald-400', icon: Calendar,      variant: 'success' },
  offer:           { label: 'Offer',            color: 'text-amber-400',   icon: Trophy,        variant: 'warning' },
  rejected:        { label: 'Rejected',         color: 'text-red-400',     icon: XCircle,       variant: 'destructive' },
  withdrawn:       { label: 'Withdrawn',        color: 'text-slate-400',   icon: ArchiveX,      variant: 'secondary' },
  manual_required: { label: 'Manual Required',  color: 'text-orange-400',  icon: CheckCircle2,  variant: 'warning' },
  discovered:      { label: 'Discovered',       color: 'text-slate-400',   icon: Clock,         variant: 'outline' },
  queued:          { label: 'Queued',           color: 'text-slate-300',   icon: Clock,         variant: 'outline' },
  archived:        { label: 'Archived',         color: 'text-slate-500',   icon: ArchiveX,      variant: 'secondary' },
}

const ACTIVE_STAGES = ['applied', 'interviewing', 'offer']

function PipelineBar({ pipeline }: { pipeline: PipelineCount }) {
  const total = Object.values(pipeline).reduce((a, b) => a + b, 0)
  return (
    <Card>
      <CardContent className="p-5">
        <div className="grid grid-cols-3 divide-x divide-border">
          {ACTIVE_STAGES.map(stage => {
            const cfg = STATUS_CONFIG[stage]
            const count = pipeline[stage] ?? 0
            const Icon = cfg.icon
            return (
              <div key={stage} className="px-6 first:pl-0 last:pr-0 flex items-center gap-3">
                <div className="w-9 h-9 rounded-md flex items-center justify-center bg-secondary border border-border">
                  <Icon className={`w-4 h-4 ${cfg.color}`} />
                </div>
                <div>
                  <p className={`font-mono text-2xl font-semibold ${cfg.color}`}>{count}</p>
                  <p className="text-xs text-muted-foreground">{cfg.label}</p>
                </div>
                <div className="ml-auto text-right">
                  <p className="font-mono text-xs text-muted-foreground">
                    {total ? Math.round(count / total * 100) : 0}%
                  </p>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}

function EmptyApplications() {
  return (
    <div className="py-14 text-center">
      <ClipboardList className="w-10 h-10 mx-auto mb-3 text-muted-foreground opacity-30" />
      <p className="text-sm text-foreground mb-1">No applications yet</p>
      <p className="text-xs text-muted-foreground">Applications appear here once jobs are discovered and auto-applied.</p>
    </div>
  )
}

export default function Applications() {
  const [statusFilter, setStatusFilter] = useState('all')
  const [localStatuses, setLocalStatuses] = useState<Record<string, string>>({})

  const pipeline = useAsync<PipelineCount>(getPipeline)
  const apps = useAsync<Application[]>(
    () => getApplications(statusFilter !== 'all' ? { status: statusFilter } : {}),
    [statusFilter]
  )

  const getStatus = (app: Application): string => localStatuses[app.id] ?? app.status

  const handleStatusChange = async (id: string, newStatus: string) => {
    setLocalStatuses(prev => ({ ...prev, [id]: newStatus }))
    try {
      await updateApplicationStatus(id, newStatus)
    } catch (_) {
      // revert on error
      setLocalStatuses(prev => { const s = { ...prev }; delete s[id]; return s })
    }
  }

  const appList = apps.data ?? []
  const p = pipeline.data ?? {}
  const rejected        = p['rejected']        ?? 0
  const manualRequired  = p['manual_required'] ?? 0
  const total           = Object.values(p).reduce((a, b) => a + b, 0)

  return (
    <div className="p-6 space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-chivo text-xl font-semibold text-foreground">Applications</h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            {pipeline.loading ? 'Loading…' : `${total} total applications`}
          </p>
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-44"><SelectValue placeholder="Filter by status" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            {Object.keys(STATUS_CONFIG).map(s => (
              <SelectItem key={s} value={s}>{STATUS_CONFIG[s].label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Pipeline overview */}
      {pipeline.loading ? (
        <div className="h-24 rounded-lg bg-card border border-border animate-pulse" />
      ) : (
        <PipelineBar pipeline={p} />
      )}

      {/* Rejected + Manual row */}
      <div className="grid grid-cols-2 gap-4">
        {[
          { key: 'rejected', count: rejected, label: 'Rejected' },
          { key: 'manual_required', count: manualRequired, label: 'Manual Required' },
        ].map(({ key, count, label }) => {
          const cfg = STATUS_CONFIG[key]
          return (
            <Card key={key}>
              <CardContent className="p-4 flex items-center gap-3">
                <p className={`font-mono text-xl font-semibold ${cfg.color}`}>{count}</p>
                <div>
                  <p className="text-sm text-foreground">{label}</p>
                  <p className="text-xs text-muted-foreground">
                    {total ? Math.round(count / total * 100) : 0}% of total
                  </p>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Table */}
      <Card>
        <CardHeader className="pb-0">
          <CardTitle className="text-sm">All Applications</CardTitle>
        </CardHeader>
        <CardContent className="p-0 pt-3">
          {apps.error && (
            <div className="px-5 py-3 text-xs text-red-400 bg-red-950/20 border-b border-red-900/30">
              Error: {apps.error}
            </div>
          )}

          <div className="grid grid-cols-[2fr_1fr_1fr_1fr_1fr] gap-3 px-5 py-2 border-b border-border text-[10px] text-muted-foreground uppercase tracking-wider font-medium">
            <span>Role</span><span>Platform</span><span>ATS Score</span><span>Applied</span><span>Status</span>
          </div>

          <div className="divide-y divide-border/40">
            {apps.loading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="px-5 py-4 flex gap-3">
                  <div className="flex-1 space-y-2">
                    <div className="h-4 w-48 rounded bg-secondary animate-pulse" />
                    <div className="h-3 w-32 rounded bg-secondary animate-pulse" />
                  </div>
                </div>
              ))
            ) : appList.length === 0 ? (
              <EmptyApplications />
            ) : appList.map(app => {
              const status = getStatus(app)
              const cfg = STATUS_CONFIG[status] ?? STATUS_CONFIG['applied']
              return (
                <div key={app.id} className="grid grid-cols-[2fr_1fr_1fr_1fr_1fr] gap-3 px-5 py-3 items-center hover:bg-accent/20 transition-colors">
                  <div className="min-w-0">
                    <p className="text-sm text-foreground font-medium truncate">{app.job_title}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <p className="text-xs text-muted-foreground">{app.company}</p>
                      {app.is_auto_applied && (
                        <Badge variant="outline" className="text-[10px] py-0 px-1">Auto</Badge>
                      )}
                    </div>
                  </div>

                  <span className="text-xs text-muted-foreground capitalize">{app.platform}</span>

                  <div className="flex flex-col gap-1">
                    {app.ats_score != null ? (
                      <>
                        <span className={`font-mono text-sm font-semibold ${
                          app.ats_score >= 80 ? 'text-emerald-400' :
                          app.ats_score >= 65 ? 'text-amber-400' : 'text-muted-foreground'
                        }`}>{Math.round(app.ats_score)}%</span>
                        <Progress value={app.ats_score} className="h-1 w-20" />
                      </>
                    ) : (
                      <span className="text-xs text-muted-foreground">—</span>
                    )}
                  </div>

                  <div>
                    <p className="text-xs text-foreground font-mono">
                      {app.applied_at ? new Date(app.applied_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) : '—'}
                    </p>
                    {app.last_status_at && app.last_status_at !== app.applied_at && (
                      <p className="text-[10px] text-muted-foreground">
                        Updated {new Date(app.last_status_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
                      </p>
                    )}
                  </div>

                  <Select value={status} onValueChange={v => handleStatusChange(app.id, v as Status)}>
                    <SelectTrigger className="h-7 w-full border-0 bg-transparent p-0 focus:ring-0 [&>svg]:hidden">
                      <Badge variant={cfg.variant} className="text-[10px] cursor-pointer">{cfg.label}</Badge>
                    </SelectTrigger>
                    <SelectContent>
                      {Object.keys(STATUS_CONFIG).map(s => (
                        <SelectItem key={s} value={s}>{STATUS_CONFIG[s].label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
