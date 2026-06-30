export type Platform = 'linkedin' | 'naukri' | 'indeed' | 'company'

export type JobStatus =
  | 'discovered'
  | 'queued'
  | 'applied'
  | 'interviewing'
  | 'offer'
  | 'rejected'
  | 'withdrawn'
  | 'manual_required'
  | 'archived'

export type EmailClassification =
  | 'interview_invite'
  | 'rejection'
  | 'assessment'
  | 'offer'
  | 'follow_up'
  | 'general'

export interface Profile {
  id: string
  name: string
  slug: string
  title: string
  summary: string
  skills: string[]
  keywords: string[]
  experience_years: number
  preferred_locations: string[]
  preferred_salary_min: number | null
  preferred_salary_max: number | null
  remote_only: boolean
  is_active: boolean
  created_at: string
}

export interface Job {
  id: string
  platform: Platform
  platform_job_id: string
  url: string
  title: string
  company: string
  location: string
  is_remote: boolean
  salary_min: number | null
  salary_max: number | null
  description: string
  is_easy_apply: boolean
  discovered_at: string
  match_score?: number
  matched_keywords?: string[]
}

export interface Application {
  id: string
  job_id: string
  profile_id: string
  status: JobStatus
  ats_score: number | null
  applied_at: string
  last_status_at: string
  notes: string
  is_auto_applied: boolean
  screenshot_path: string | null
  // Joined fields
  job_title: string
  company: string
  job_url: string
  platform: Platform
  profile_name?: string
}

export interface TailorResult {
  variant_id: string
  ats_score: number
  keyword_coverage: number
  matched_keywords: string[]
  missing_keywords: string[]
  injected_keywords: string[]
  recommendations: string[]
  reasoning: string
  pdf_path: string
}

export interface ResumeVariant {
  id: string
  profile_id: string
  job_id: string
  ats_score: number | null
  keyword_coverage: number | null
  injected_keywords: string[]
  created_at: string
}

export interface EmailThread {
  id: string
  application_id: string | null
  gmail_thread_id: string
  subject: string
  sender: string
  snippet: string
  classification: EmailClassification
  confidence: number
  received_at: string
  is_read: boolean
}

export interface Notification {
  id: string
  type: string
  title: string
  body: string
  is_read: boolean
  created_at: string
}

export interface PipelineCount {
  [status: string]: number
}

export interface ATSResult {
  score: number
  keyword_coverage: number
  matched_keywords: string[]
  missing_keywords: string[]
  formatting_score: number
  length_ok: boolean
  recommendations: string[]
}
