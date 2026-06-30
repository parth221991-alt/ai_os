import { useState, useEffect } from 'react'
import {
  X, ExternalLink, Sparkles, Download, CheckCircle2,
  Loader2, AlertCircle, ChevronRight,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Progress } from '@/components/ui/progress'
import { createApplication, tailorResume, getResumeDownloadUrl } from '@/lib/api'
import type { Job, Profile, Application, TailorResult } from '@/types'

const PLATFORM_COLORS: Record<string, string> = {
  linkedin: 'text-sky-400 border-sky-900/40 bg-sky-950/40',
  naukri:   'text-orange-400 border-orange-900/40 bg-orange-950/40',
  indeed:   'text-blue-400 border-blue-900/40 bg-blue-950/40',
  company:  'text-purple-400 border-purple-900/40 bg-purple-950/40',
}
const PLATFORM_LABEL: Record<string, string> = {
  linkedin: 'LinkedIn', naukri: 'Naukri', indeed: 'Indeed', company: 'Company',
}

type TailorState = 'idle' | 'loading' | 'done' | 'error'
type ApplyState  = 'idle' | 'loading' | 'done' | 'conflict' | 'error'

interface Props {
  job: Job | null
  profiles: Profile[]
  defaultProfileId: string
  existingApplication?: Application
  onClose: () => void
  onApplied: (jobId: string, app: Application) => void
}

export default function ApplyDrawer({
  job,
  profiles,
  defaultProfileId,
  existingApplication,
  onClose,
  onApplied,
}: Props) {
  const [profileId, setProfileId]     = useState(defaultProfileId || profiles[0]?.id || '')
  const [tailorState, setTailorState] = useState<TailorState>('idle')
  const [tailored, setTailored]       = useState<TailorResult | null>(null)
  const [tailorError, setTailorError] = useState('')
  const [applyState, setApplyState]   = useState<ApplyState>(existingApplication ? 'done' : 'idle')
  const [applyError, setApplyError]   = useState('')
  const [appliedApp, setAppliedApp]   = useState<Application | null>(existingApplication ?? null)

  // Reset state when job changes
  useEffect(() => {
    setProfileId(defaultProfileId || profiles[0]?.id || '')
    setTailorState('idle')
    setTailored(null)
    setTailorError('')
    if (existingApplication) {
      setApplyState('done')
      setAppliedApp(existingApplication)
    } else {
      setApplyState('idle')
      setAppliedApp(null)
    }
    setApplyError('')
  }, [job?.id, defaultProfileId, existingApplication])

  const selectedProfile = profiles.find(p => p.id === profileId)
  const score = job?.match_score

  const handleTailor = async () => {
    if (!job || !profileId) return
    setTailorState('loading')
    setTailorError('')
    try {
      const result = await tailorResume(profileId, job.id)
      setTailored(result)
      setTailorState('done')
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Tailoring failed'
      setTailorError(msg.includes('404') ? 'No base resume found for this profile. Upload one in Profiles.' : msg)
      setTailorState('error')
    }
  }

  const handleApply = async () => {
    if (!job || !profileId) return
    setApplyState('loading')
    setApplyError('')
    try {
      const notes = tailored ? `Resume variant: ${tailored.variant_id}` : ''
      const app = await createApplication({ job_id: job.id, profile_id: profileId, notes })
      setAppliedApp(app)
      setApplyState('done')
      window.open(job.url, '_blank', 'noopener,noreferrer')
      onApplied(job.id, app)
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Apply failed'
      if (msg.includes('409')) {
        setApplyState('conflict')
        setApplyError('Already applied to this job with this profile.')
      } else {
        setApplyState('error')
        setApplyError(msg)
      }
    }
  }

  const isOpen = job !== null

  return (
    <>
      {/* Backdrop */}
      <div
        className={`fixed inset-0 bg-black/50 z-40 transition-opacity duration-200 ${
          isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        onClick={onClose}
      />

      {/* Drawer panel */}
      <div
        className={`fixed top-0 right-0 h-full w-[480px] bg-background border-l border-border z-50
          flex flex-col shadow-2xl transition-transform duration-200 ease-out ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        {!job ? null : (
          <>
            {/* Header */}
            <div className="flex items-start justify-between px-6 pt-5 pb-4 border-b border-border shrink-0">
              <div className="min-w-0 flex-1 pr-4">
                <div className="flex items-center gap-2 flex-wrap mb-1">
                  <span className={`inline-flex text-[10px] px-2 py-0.5 rounded-full border font-medium ${PLATFORM_COLORS[job.platform] ?? ''}`}>
                    {PLATFORM_LABEL[job.platform] ?? job.platform}
                  </span>
                  {job.is_easy_apply && (
                    <Badge variant="success" className="text-[10px] py-0 px-1.5">Easy Apply</Badge>
                  )}
                </div>
                <h2 className="font-chivo text-base font-semibold text-foreground leading-tight">{job.title}</h2>
                <p className="text-sm text-muted-foreground mt-0.5">{job.company}</p>
                {job.location && (
                  <p className="text-xs text-muted-foreground mt-0.5">{job.location}</p>
                )}
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <a
                  href={job.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-muted-foreground hover:text-foreground transition-colors"
                  title="Open job listing"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
                <button onClick={onClose} className="text-muted-foreground hover:text-foreground transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Scrollable body */}
            <div className="flex-1 overflow-y-auto px-6 py-5 space-y-6">

              {/* Match score */}
              {score != null && (
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs text-muted-foreground uppercase tracking-wider font-medium">Match Score</span>
                    <span className={`font-mono text-sm font-semibold ${
                      score >= 85 ? 'text-emerald-400' : score >= 70 ? 'text-amber-400' : 'text-muted-foreground'
                    }`}>{Math.round(score)}%</span>
                  </div>
                  <Progress value={score} className="h-1.5" />
                </div>
              )}

              {/* Profile picker */}
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wider font-medium mb-2">Apply with Profile</p>
                <Select value={profileId} onValueChange={v => {
                  setProfileId(v)
                  setTailorState('idle')
                  setTailored(null)
                }}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose profile…" />
                  </SelectTrigger>
                  <SelectContent>
                    {profiles.map(p => (
                      <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {selectedProfile && (
                  <p className="text-[11px] text-muted-foreground mt-1.5 leading-relaxed line-clamp-2">
                    {selectedProfile.title} · {selectedProfile.experience_years}yr exp
                  </p>
                )}
              </div>

              {/* Tailor Resume */}
              <div className="border border-border rounded-lg p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-foreground">Tailor Resume with Claude</p>
                    <p className="text-[11px] text-muted-foreground mt-0.5">
                      Rewrites your resume to match this JD and injects missing keywords.
                    </p>
                  </div>
                  <Badge variant="outline" className="text-[10px]">Optional</Badge>
                </div>

                {tailorState === 'idle' && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={handleTailor}
                    disabled={!profileId}
                    className="w-full gap-2"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    Tailor with Claude
                  </Button>
                )}

                {tailorState === 'loading' && (
                  <div className="flex items-center gap-3 py-2 text-sm text-muted-foreground">
                    <Loader2 className="w-4 h-4 animate-spin shrink-0" />
                    <span>Claude is rewriting your resume… (~15s)</span>
                  </div>
                )}

                {tailorState === 'error' && (
                  <div className="space-y-2">
                    <div className="flex items-start gap-2 text-xs text-red-400">
                      <AlertCircle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                      <span>{tailorError}</span>
                    </div>
                    <Button size="sm" variant="outline" onClick={handleTailor} className="w-full gap-2">
                      <Sparkles className="w-3.5 h-3.5" />
                      Retry
                    </Button>
                  </div>
                )}

                {tailorState === 'done' && tailored && (
                  <div className="space-y-3">
                    {/* ATS score */}
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-muted-foreground">Tailored ATS Score</span>
                      <span className={`font-mono text-sm font-semibold ${
                        tailored.ats_score >= 85 ? 'text-emerald-400' :
                        tailored.ats_score >= 70 ? 'text-amber-400' : 'text-muted-foreground'
                      }`}>{Math.round(tailored.ats_score)}%</span>
                    </div>
                    <Progress value={tailored.ats_score} className="h-1" />

                    {/* Injected keywords */}
                    {tailored.injected_keywords.length > 0 && (
                      <div>
                        <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1.5">Injected Keywords</p>
                        <div className="flex flex-wrap gap-1">
                          {tailored.injected_keywords.slice(0, 8).map(kw => (
                            <span key={kw} className="text-[10px] bg-emerald-950/40 text-emerald-300 px-1.5 py-0.5 rounded border border-emerald-900/30">
                              +{kw}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Missing keywords */}
                    {tailored.missing_keywords.length > 0 && (
                      <div>
                        <p className="text-[10px] text-muted-foreground uppercase tracking-wider mb-1.5">Still Missing</p>
                        <div className="flex flex-wrap gap-1">
                          {tailored.missing_keywords.slice(0, 5).map(kw => (
                            <span key={kw} className="text-[10px] bg-red-950/30 text-red-400 px-1.5 py-0.5 rounded border border-red-900/30">
                              {kw}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Download */}
                    <a
                      href={getResumeDownloadUrl(tailored.variant_id)}
                      download
                      className="flex items-center gap-2 text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
                    >
                      <Download className="w-3.5 h-3.5" />
                      Download Tailored PDF
                    </a>
                  </div>
                )}
              </div>

              {/* Apply action */}
              <div className="space-y-3">
                {applyState === 'done' || applyState === 'conflict' ? (
                  <div className="rounded-lg bg-emerald-950/30 border border-emerald-900/40 p-4 space-y-2">
                    <div className="flex items-center gap-2 text-emerald-400">
                      <CheckCircle2 className="w-4 h-4 shrink-0" />
                      <span className="text-sm font-medium">
                        Applied{appliedApp?.applied_at
                          ? ` on ${new Date(appliedApp.applied_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}`
                          : ''}
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Track the outcome in Applications.
                    </p>
                    <button
                      onClick={onClose}
                      className="flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
                    >
                      View Applications <ChevronRight className="w-3 h-3" />
                    </button>
                  </div>
                ) : (
                  <>
                    <Button
                      className="w-full gap-2"
                      onClick={handleApply}
                      disabled={applyState === 'loading' || !profileId}
                    >
                      {applyState === 'loading' ? (
                        <><Loader2 className="w-3.5 h-3.5 animate-spin" />Recording…</>
                      ) : (
                        <><ExternalLink className="w-3.5 h-3.5" />Open & Mark as Applied</>
                      )}
                    </Button>

                    {applyState === 'error' && (
                      <div className="flex items-start gap-2 text-xs text-red-400">
                        <AlertCircle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                        <span>{applyError}</span>
                      </div>
                    )}

                    <p className="text-[11px] text-muted-foreground text-center leading-relaxed">
                      Opens the job listing in a new tab and records this application so you can track its status.
                    </p>
                  </>
                )}
              </div>

            </div>
          </>
        )}
      </div>
    </>
  )
}
