import { useState } from 'react'
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts'
import { Briefcase, Send, CalendarCheck, Bell, Play, RefreshCw, TrendingUp, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { useAsync } from '@/hooks/useAsync'
import { getPipeline, getJobs, getNotifications, triggerDiscovery, markNotificationRead } from '@/lib/api'
import type { Job, Notification, PipelineCount } from '@/types'

// Static chart data (no historical endpoint yet)
const weeklyTrend = [
  { day: 'Mon', applied: 0, discovered: 0 },
  { day: 'Tue', applied: 0, discovered: 0 },
  { day: 'Wed', applied: 0, discovered: 0 },
  { day: 'Thu', applied: 0, discovered: 0 },
  { day: 'Fri', applied: 0, discovered: 0 },
  { day: 'Sat', applied: 0, discovered: 0 },
  { day: 'Sun', applied: 0, discovered: 0 },
]

const PIPELINE_COLORS: Record<string, string> = {
  applied:         '#6366f1',
  interviewing:    '#10b981',
  offer:           '#f59e0b',
  rejected:        '#ef4444',
  manual_required: '#f97316',
  discovered:      '#64748b',
  queued:          '#94a3b8',
}

const PLATFORM_LABEL: Record<string, string> = {
  linkedin: 'LinkedIn',
  naukri: 'Naukri',
  indeed: 'Indeed',
  company: 'Company',
}

const tooltipStyle = {
  backgroundColor: '#0f172a',
  border: '1px solid #1e293b',
  borderRadius: '6px',
  color: '#e2e8f0',
  fontSize: '11px',
}

function KpiCard({
  label, value, sub, icon: Icon, trend, color, bgColor,
}: {
  label: string; value: string | number; sub: string
  icon: React.FC<{ className?: string }>
  trend?: number; color: string; bgColor: string
}) {
  return (
    <Card>
      <CardContent className="p-5">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs text-muted-foreground mb-1">{label}</p>
            <p className={`font-mono text-2xl font-semibold ${color}`}>{value}</p>
            <p className="text-xs text-muted-foreground mt-1">{sub}</p>
          </div>
          <div className={`w-9 h-9 rounded-md flex items-center justify-center ${bgColor} border border-white/5`}>
            <Icon className={`w-4 h-4 ${color}`} />
          </div>
        </div>
        {trend !== undefined && (
          <div className="mt-3">
            <Progress value={trend} />
            <p className="text-[10px] text-muted-foreground mt-1">{trend}% of daily goal</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

function EmptyJobs() {
  return (
    <div className="py-8 text-center text-muted-foreground">
      <Briefcase className="w-8 h-8 mx-auto mb-2 opacity-30" />
      <p className="text-sm">No jobs discovered yet.</p>
      <p className="text-xs mt-1">Click "Run Discovery" to start scraping.</p>
    </div>
  )
}

function EmptyNotifications() {
  return (
    <div className="py-6 text-center text-muted-foreground">
      <Bell className="w-6 h-6 mx-auto mb-2 opacity-30" />
      <p className="text-sm">No unread notifications.</p>
    </div>
  )
}

export default function Dashboard() {
  const [discovering, setDiscovering] = useState(false)

  const pipeline = useAsync<PipelineCount>(getPipeline)
  const recentJobs = useAsync<Job[]>(() => getJobs({ limit: 5 }))
  const notifications = useAsync<Notification[]>(() => getNotifications(true))

  const handleDiscovery = async () => {
    setDiscovering(true)
    try { await triggerDiscovery() } catch (_) { /* swallow */ }
    setTimeout(() => {
      setDiscovering(false)
      pipeline.reload()
      recentJobs.reload()
    }, 3000)
  }

  const handleMarkRead = async (id: string) => {
    await markNotificationRead(id)
    notifications.reload()
  }

  const p = pipeline.data ?? {}
  const totalApps = Object.values(p).reduce((a, b) => a + b, 0)
  const applied      = p['applied']      ?? 0
  const interviewing = p['interviewing'] ?? 0
  const offer        = p['offer']        ?? 0
  const rejected     = p['rejected']     ?? 0
  const notifCount   = (notifications.data ?? []).length

  const pipelineChartData = Object.entries(p)
    .filter(([, v]) => v > 0)
    .map(([name, value]) => ({ name, value, color: PIPELINE_COLORS[name] ?? '#64748b' }))

  // Build platform bar data from recent jobs
  const platformCounts: Record<string, number> = {}
  for (const job of recentJobs.data ?? []) {
    platformCounts[job.platform] = (platformCounts[job.platform] ?? 0) + 1
  }
  const platformData = Object.entries(platformCounts).map(([platform, count]) => ({
    platform: PLATFORM_LABEL[platform] ?? platform,
    count,
  }))

  return (
    <div className="p-6 space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-chivo text-xl font-semibold text-foreground">Dashboard</h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            {new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'short', year: 'numeric' })}
            {' · Next run 08:00 IST'}
          </p>
        </div>
        <Button onClick={handleDiscovery} disabled={discovering} size="sm">
          {discovering ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5" />}
          {discovering ? 'Running...' : 'Run Discovery'}
        </Button>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-4 gap-4">
        <KpiCard label="Total Jobs"    value={recentJobs.data?.length ?? 0} sub="In database"  icon={Briefcase}    color="text-indigo-400" bgColor="bg-indigo-950/60" />
        <KpiCard label="Applied"       value={applied}                       sub={`of ${totalApps} total`} icon={Send} trend={totalApps ? Math.round(applied / totalApps * 100) : 0} color="text-sky-400" bgColor="bg-sky-950/60" />
        <KpiCard label="Interviewing"  value={interviewing + offer}           sub={offer > 0 ? `${offer} offer${offer > 1 ? 's' : ''}` : 'Active'}  icon={CalendarCheck} color="text-emerald-400" bgColor="bg-emerald-950/60" />
        <KpiCard label="Alerts"        value={notifCount}                     sub="Unread"      icon={Bell}          color="text-amber-400"  bgColor="bg-amber-950/60" />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-3 gap-4">
        {/* Weekly activity (static skeleton until historical data endpoint exists) */}
        <Card className="col-span-2">
          <CardHeader className="pb-0">
            <CardTitle className="text-sm">Weekly Activity</CardTitle>
          </CardHeader>
          <CardContent className="pt-3">
            <ResponsiveContainer width="100%" height={180}>
              <AreaChart data={weeklyTrend} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="gDisc" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#6366f1" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gAppl" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#10b981" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="day" tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={tooltipStyle} />
                <Area type="monotone" dataKey="discovered" stroke="#6366f1" fill="url(#gDisc)" strokeWidth={1.5} name="Discovered" />
                <Area type="monotone" dataKey="applied"    stroke="#10b981" fill="url(#gAppl)" strokeWidth={1.5} name="Applied" />
              </AreaChart>
            </ResponsiveContainer>
            <div className="flex gap-4 mt-1">
              <span className="flex items-center gap-1.5 text-[10px] text-muted-foreground"><span className="w-2 h-2 rounded-full bg-indigo-500" />Discovered</span>
              <span className="flex items-center gap-1.5 text-[10px] text-muted-foreground"><span className="w-2 h-2 rounded-full bg-emerald-500" />Applied</span>
            </div>
          </CardContent>
        </Card>

        {/* Pipeline donut */}
        <Card>
          <CardHeader className="pb-0">
            <CardTitle className="text-sm">Pipeline</CardTitle>
          </CardHeader>
          <CardContent className="pt-3">
            {pipeline.loading ? (
              <div className="h-40 flex items-center justify-center text-muted-foreground text-xs">Loading…</div>
            ) : pipelineChartData.length === 0 ? (
              <div className="h-40 flex flex-col items-center justify-center text-muted-foreground gap-2">
                <AlertCircle className="w-6 h-6 opacity-30" />
                <p className="text-xs">No applications yet</p>
              </div>
            ) : (
              <>
                <ResponsiveContainer width="100%" height={140}>
                  <PieChart>
                    <Pie data={pipelineChartData} cx="50%" cy="50%" innerRadius={42} outerRadius={62} dataKey="value" strokeWidth={0}>
                      {pipelineChartData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                    </Pie>
                    <Tooltip contentStyle={tooltipStyle} />
                  </PieChart>
                </ResponsiveContainer>
                <div className="grid grid-cols-2 gap-x-3 gap-y-1.5 mt-2">
                  {pipelineChartData.map(d => (
                    <div key={d.name} className="flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full shrink-0" style={{ background: d.color }} />
                      <span className="text-[10px] text-muted-foreground capitalize truncate">{d.name.replace('_', ' ')}</span>
                      <span className="font-mono text-[10px] text-foreground ml-auto">{d.value}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-3 gap-4">
        {/* Platform bar */}
        <Card>
          <CardHeader className="pb-0">
            <CardTitle className="text-sm">By Platform</CardTitle>
          </CardHeader>
          <CardContent className="pt-3">
            {platformData.length === 0 ? (
              <div className="h-[120px] flex items-center justify-center text-xs text-muted-foreground">No data yet</div>
            ) : (
              <ResponsiveContainer width="100%" height={120}>
                <BarChart data={platformData} layout="vertical" margin={{ top: 0, right: 8, left: 0, bottom: 0 }}>
                  <XAxis type="number" tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis dataKey="platform" type="category" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} width={52} />
                  <Tooltip contentStyle={tooltipStyle} />
                  <Bar dataKey="count" fill="#6366f1" radius={[0, 3, 3, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>

        {/* Top matches */}
        <Card className="col-span-2">
          <CardHeader className="pb-0 flex flex-row items-center justify-between">
            <CardTitle className="text-sm">Recent Jobs</CardTitle>
            <TrendingUp className="w-3.5 h-3.5 text-muted-foreground" />
          </CardHeader>
          <CardContent className="pt-3">
            {recentJobs.loading ? (
              <div className="space-y-3">
                {[1,2,3].map(i => <div key={i} className="h-10 rounded bg-secondary animate-pulse" />)}
              </div>
            ) : (recentJobs.data ?? []).length === 0 ? (
              <EmptyJobs />
            ) : (
              <div className="space-y-0">
                {(recentJobs.data ?? []).map(job => (
                  <div key={job.id} className="flex items-center gap-3 py-2.5 border-b border-border/40 last:border-0">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-foreground truncate">{job.title}</p>
                      <p className="text-xs text-muted-foreground">{job.company}</p>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      {job.is_easy_apply && <Badge variant="success" className="text-[10px] py-0 px-1.5">Easy</Badge>}
                      <Badge variant="outline" className="text-[10px] py-0 px-1.5 capitalize">{job.platform}</Badge>
                      {job.match_score != null && (
                        <span className={`font-mono text-sm font-semibold w-10 text-right ${
                          job.match_score >= 85 ? 'text-emerald-400' : job.match_score >= 70 ? 'text-amber-400' : 'text-muted-foreground'
                        }`}>{Math.round(job.match_score)}%</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Notifications */}
      <Card>
        <CardHeader className="pb-0 flex flex-row items-center justify-between">
          <CardTitle className="text-sm">Unread Alerts</CardTitle>
          {notifCount > 0 && (
            <Badge variant="warning" className="text-[10px]">{notifCount} unread</Badge>
          )}
        </CardHeader>
        <CardContent className="pt-3">
          {notifications.loading ? (
            <div className="space-y-2">
              {[1,2].map(i => <div key={i} className="h-8 rounded bg-secondary animate-pulse" />)}
            </div>
          ) : (notifications.data ?? []).length === 0 ? (
            <EmptyNotifications />
          ) : (
            <div className="space-y-0">
              {(notifications.data ?? []).map(n => (
                <div key={n.id} className="flex items-center gap-3 py-2.5 border-b border-border/40 last:border-0">
                  <div className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                    n.type === 'interview_invite' ? 'bg-emerald-400' :
                    n.type === 'offer'            ? 'bg-amber-400' :
                    n.type === 'rejection'        ? 'bg-red-400' : 'bg-indigo-400'
                  }`} />
                  <p className="flex-1 text-sm text-foreground">{n.title}</p>
                  <p className="text-xs text-muted-foreground">{n.body?.slice(0, 60)}</p>
                  <button
                    onClick={() => handleMarkRead(n.id)}
                    className="text-[10px] text-muted-foreground hover:text-foreground transition-colors"
                  >
                    Mark read
                  </button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
