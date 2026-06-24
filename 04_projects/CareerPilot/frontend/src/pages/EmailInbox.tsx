import { useState } from 'react'
import { RefreshCw, Mail, MailOpen, Calendar, Trophy, XCircle, FileText, MessageSquare } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useAsync } from '@/hooks/useAsync'
import { getEmailThreads, syncEmails } from '@/lib/api'
import type { EmailThread, EmailClassification } from '@/types'

const CLASS_CONFIG: Record<EmailClassification, {
  label: string
  variant: 'default' | 'success' | 'destructive' | 'warning' | 'outline' | 'secondary' | 'info'
  icon: React.FC<{ className?: string }>
  color: string
}> = {
  interview_invite: { label: 'Interview',  variant: 'success',     icon: Calendar,      color: 'text-emerald-400' },
  offer:            { label: 'Offer',      variant: 'warning',     icon: Trophy,        color: 'text-amber-400' },
  assessment:       { label: 'Assessment', variant: 'default',     icon: FileText,      color: 'text-indigo-400' },
  rejection:        { label: 'Rejected',   variant: 'destructive', icon: XCircle,       color: 'text-red-400' },
  follow_up:        { label: 'Follow-up',  variant: 'secondary',   icon: MessageSquare, color: 'text-slate-400' },
  general:          { label: 'General',    variant: 'outline',     icon: Mail,          color: 'text-muted-foreground' },
}

const ACTION_TYPES: EmailClassification[] = ['interview_invite', 'offer', 'assessment']

const TABS = [
  { value: 'all',             label: 'All' },
  { value: 'interview_invite',label: 'Interviews' },
  { value: 'offer',           label: 'Offers' },
  { value: 'assessment',      label: 'Assessments' },
  { value: 'rejection',       label: 'Rejections' },
]

function EmptyInbox() {
  return (
    <div className="py-14 text-center">
      <Mail className="w-10 h-10 mx-auto mb-3 text-muted-foreground opacity-30" />
      <p className="text-sm text-foreground mb-1">No career emails yet</p>
      <p className="text-xs text-muted-foreground">
        Connect Gmail OAuth in Settings, then sync to classify incoming emails.
      </p>
    </div>
  )
}

export default function EmailInbox() {
  const [tab, setTab]       = useState('all')
  const [readSet, setReadSet] = useState<Set<string>>(new Set())
  const [syncing, setSyncing] = useState(false)

  const threads = useAsync<EmailThread[]>(
    () => getEmailThreads(tab !== 'all' ? tab : undefined),
    [tab]
  )

  const allThreads = threads.data ?? []
  const unreadCount = allThreads.filter(e => !e.is_read && !readSet.has(e.id)).length
  const actionRequired = allThreads.filter(e => ACTION_TYPES.includes(e.classification))

  const handleSync = async () => {
    setSyncing(true)
    try { await syncEmails() } catch (_) { /* gmail not configured yet */ }
    setTimeout(() => { setSyncing(false); threads.reload() }, 2000)
  }

  const markRead = (id: string) => setReadSet(prev => { const s = new Set(prev); s.add(id); return s })

  const classCount = (cls: EmailClassification) => allThreads.filter(e => e.classification === cls).length

  return (
    <div className="p-6 space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-chivo text-xl font-semibold text-foreground">Email Inbox</h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            {threads.loading ? 'Loading…' : `${unreadCount} unread · Claude-classified`}
          </p>
        </div>
        <Button size="sm" variant="outline" onClick={handleSync} disabled={syncing}>
          <RefreshCw className={`w-3.5 h-3.5 ${syncing ? 'animate-spin' : ''}`} />
          {syncing ? 'Syncing…' : 'Sync Now'}
        </Button>
      </div>

      {/* Action required banner */}
      {actionRequired.length > 0 && (
        <Card className="border-amber-900/40 bg-amber-950/10">
          <CardContent className="p-4">
            <p className="text-xs font-medium text-amber-400 mb-2">Action Required ({actionRequired.length})</p>
            <div className="space-y-2">
              {actionRequired.map(e => {
                const cfg = CLASS_CONFIG[e.classification]
                const Icon = cfg.icon
                return (
                  <div key={e.id} className="flex items-center gap-3">
                    <Icon className={`w-3.5 h-3.5 shrink-0 ${cfg.color}`} />
                    <p className="text-xs text-foreground flex-1 truncate">{e.subject}</p>
                    <p className="text-[10px] text-muted-foreground">{e.sender?.split('@')[1] ?? ''}</p>
                    <Badge variant={cfg.variant} className="text-[10px] shrink-0">{cfg.label}</Badge>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Category stats */}
      <div className="grid grid-cols-6 gap-3">
        {(Object.keys(CLASS_CONFIG) as EmailClassification[]).map(key => {
          const cfg = CLASS_CONFIG[key]
          const Icon = cfg.icon
          const count = classCount(key)
          return (
            <Card key={key} className="cursor-pointer hover:border-border/80 transition-colors" onClick={() => setTab(key)}>
              <CardContent className="p-3 text-center">
                <Icon className={`w-4 h-4 mx-auto mb-1 ${cfg.color}`} />
                <p className={`font-mono text-lg font-semibold ${cfg.color}`}>{count}</p>
                <p className="text-[10px] text-muted-foreground">{cfg.label}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Thread list */}
      <Card>
        <CardHeader className="pb-0 px-5 pt-4">
          <Tabs value={tab} onValueChange={setTab}>
            <TabsList>
              {TABS.map(t => (
                <TabsTrigger key={t.value} value={t.value}>
                  {t.label}
                  {t.value !== 'all' && (
                    <span className="ml-1 font-mono text-[10px]">
                      ({classCount(t.value as EmailClassification)})
                    </span>
                  )}
                </TabsTrigger>
              ))}
            </TabsList>
          </Tabs>
        </CardHeader>
        <CardContent className="p-0 pt-3">
          {threads.error && (
            <div className="px-5 py-3 text-xs text-red-400 bg-red-950/20 border-b border-red-900/30">
              Error: {threads.error}
            </div>
          )}

          <div className="divide-y divide-border/40">
            {threads.loading ? (
              Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="px-5 py-4 flex gap-4">
                  <div className="w-8 h-8 rounded-md bg-secondary animate-pulse shrink-0" />
                  <div className="flex-1 space-y-2">
                    <div className="h-4 w-64 rounded bg-secondary animate-pulse" />
                    <div className="h-3 w-40 rounded bg-secondary animate-pulse" />
                  </div>
                </div>
              ))
            ) : allThreads.length === 0 ? (
              <EmptyInbox />
            ) : allThreads.map(email => {
              const cfg = CLASS_CONFIG[email.classification] ?? CLASS_CONFIG.general
              const Icon = cfg.icon
              const isRead = email.is_read || readSet.has(email.id)
              return (
                <div
                  key={email.id}
                  className={`px-5 py-4 flex gap-4 cursor-pointer hover:bg-accent/20 transition-colors ${!isRead ? 'bg-accent/10' : ''}`}
                  onClick={() => markRead(email.id)}
                >
                  {/* Icon */}
                  <div className={`w-8 h-8 rounded-md flex items-center justify-center shrink-0 ${
                    isRead ? 'bg-secondary' : 'bg-indigo-950/60 border border-indigo-900/40'
                  }`}>
                    {isRead
                      ? <MailOpen className="w-4 h-4 text-muted-foreground" />
                      : <Mail className="w-4 h-4 text-indigo-400" />}
                  </div>

                  {/* Body */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start gap-2 justify-between">
                      <div className="min-w-0">
                        <p className={`text-sm truncate ${!isRead ? 'font-semibold text-foreground' : 'text-foreground'}`}>
                          {email.subject || '(no subject)'}
                        </p>
                        <p className="text-xs text-muted-foreground mt-0.5">{email.sender}</p>
                      </div>
                      <span className="text-[10px] text-muted-foreground font-mono shrink-0">
                        {email.received_at
                          ? new Date(email.received_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })
                          : '—'}
                      </span>
                    </div>
                    {email.snippet && (
                      <p className="text-xs text-muted-foreground mt-1.5 line-clamp-1">{email.snippet}</p>
                    )}
                    <div className="flex items-center gap-2 mt-2">
                      <Badge variant={cfg.variant} className="text-[10px] gap-1">
                        <Icon className="w-2.5 h-2.5" />{cfg.label}
                      </Badge>
                      {email.confidence != null && (
                        <span className="text-[10px] text-muted-foreground font-mono">
                          {Math.round(email.confidence * 100)}% confidence
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
