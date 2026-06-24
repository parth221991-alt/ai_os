import type {
  Application, ATSResult, EmailThread, Job,
  Notification, PipelineCount, Profile,
} from '@/types'

const BASE = 'http://localhost:8005'

async function req<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText)
    throw new Error(`${res.status}: ${text}`)
  }
  return res.json() as Promise<T>
}

function qs(params: Record<string, string | number | boolean | undefined | null>): string {
  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
  if (!entries.length) return ''
  return '?' + new URLSearchParams(entries.map(([k, v]) => [k, String(v)])).toString()
}

// ── Profiles ─────────────────────────────────────────────────────────────────

export const getProfiles = () =>
  req<Profile[]>('/profiles/')

export const createProfile = (data: {
  name: string; slug: string; title: string; summary?: string
  skills?: string[]; keywords?: string[]; experience_years?: number
  preferred_locations?: string[]; remote_only?: boolean
}) => req<Profile>('/profiles/', { method: 'POST', body: JSON.stringify(data) })

export const updateProfile = (id: string, data: Partial<Profile>) =>
  req<Profile>(`/profiles/${id}`, { method: 'PATCH', body: JSON.stringify(data) })

export const getProfileResumes = (profileId: string) =>
  req<object[]>(`/profiles/${profileId}/resumes`)

export const uploadBaseResume = (profileId: string, data: { content: object; raw_text: string }) =>
  req<object>(`/profiles/${profileId}/resumes`, { method: 'POST', body: JSON.stringify(data) })

// ── Jobs ─────────────────────────────────────────────────────────────────────

export interface JobsQuery {
  platform?: string
  min_score?: number
  profile_id?: string
  limit?: number
  offset?: number
  [key: string]: string | number | boolean | undefined | null
}

export const getJobs = (params: JobsQuery = {}) =>
  req<Job[]>(`/jobs/${qs(params)}`)

export const getJob = (id: string) =>
  req<Job>(`/jobs/${id}`)

export const triggerDiscovery = () =>
  req<{ message: string }>('/jobs/discover', { method: 'POST' })

// ── Applications ──────────────────────────────────────────────────────────────

export interface ApplicationsQuery {
  status?: string
  profile_id?: string
  [key: string]: string | undefined
}

export const getApplications = (params: ApplicationsQuery = {}) =>
  req<Application[]>(`/applications/${qs(params)}`)

export const getPipeline = () =>
  req<PipelineCount>('/applications/pipeline')

export const createApplication = (data: { job_id: string; profile_id: string; notes?: string }) =>
  req<Application>('/applications/', { method: 'POST', body: JSON.stringify(data) })

export const updateApplicationStatus = (id: string, status: string, notes?: string) =>
  req<Application>(`/applications/${id}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status, notes }),
  })

export const retryApply = (id: string) =>
  req<{ message: string }>(`/applications/${id}/apply`, { method: 'POST' })

// ── Resume ────────────────────────────────────────────────────────────────────

export const tailorResume = (profile_id: string, job_id: string) =>
  req<object>('/resume/tailor', {
    method: 'POST',
    body: JSON.stringify({ profile_id, job_id }),
  })

export const scoreATS = (resume_text: string, job_description: string) =>
  req<ATSResult>('/resume/ats-score', {
    method: 'POST',
    body: JSON.stringify({ resume_text, job_description }),
  })

export const getResumeDownloadUrl = (variantId: string) =>
  `${BASE}/resume/${variantId}/download`

// ── Email ─────────────────────────────────────────────────────────────────────

export const getEmailThreads = (classification?: string) =>
  req<EmailThread[]>(`/email/threads${classification ? `?classification=${classification}` : ''}`)

export const syncEmails = () =>
  req<{ message: string }>('/email/sync', { method: 'POST' })

export const getNotifications = (unreadOnly = true) =>
  req<Notification[]>(`/email/notifications?unread_only=${unreadOnly}`)

export const markNotificationRead = (id: string) =>
  req<{ ok: boolean }>(`/email/notifications/${id}/read`, { method: 'PATCH' })
