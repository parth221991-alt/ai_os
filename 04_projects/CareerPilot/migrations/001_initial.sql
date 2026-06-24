-- CareerPilot initial schema
-- Run once against your PostgreSQL database
-- Tables are also auto-created by SQLAlchemy on startup (Base.metadata.create_all)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Profiles: one row per career persona
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    summary TEXT,
    skills TEXT[],
    keywords TEXT[],
    experience_years INTEGER,
    preferred_locations TEXT[],
    preferred_salary_min INTEGER,
    preferred_salary_max INTEGER,
    remote_only BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Base resumes: versioned master resume per profile
CREATE TABLE IF NOT EXISTS base_resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    version INTEGER DEFAULT 1,
    content JSONB NOT NULL,
    raw_text TEXT,
    file_path VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Jobs: all discovered job postings
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform VARCHAR(50) NOT NULL,
    platform_job_id VARCHAR(200),
    url TEXT NOT NULL,
    title VARCHAR(300) NOT NULL,
    company VARCHAR(200) NOT NULL,
    location VARCHAR(200),
    is_remote BOOLEAN DEFAULT FALSE,
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(10) DEFAULT 'INR',
    description TEXT,
    requirements TEXT,
    posted_at TIMESTAMPTZ,
    discovered_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    is_easy_apply BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    raw_data JSONB,
    CONSTRAINT uq_platform_job UNIQUE (platform, platform_job_id)
);

CREATE INDEX IF NOT EXISTS ix_jobs_discovered_at ON jobs(discovered_at);
CREATE INDEX IF NOT EXISTS ix_jobs_company ON jobs(company);

-- Job match scores: per-profile relevance score for each job
CREATE TABLE IF NOT EXISTS job_match_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    score FLOAT NOT NULL,
    keyword_matches TEXT[],
    missing_keywords TEXT[],
    reasoning TEXT,
    scored_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_job_profile_score UNIQUE (job_id, profile_id)
);

-- Resume variants: Claude-tailored resume per job application
CREATE TABLE IF NOT EXISTS resume_variants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id UUID REFERENCES profiles(id),
    job_id UUID REFERENCES jobs(id),
    base_resume_id UUID REFERENCES base_resumes(id),
    tailored_content JSONB NOT NULL,
    raw_text TEXT,
    pdf_path VARCHAR(500),
    ats_score FLOAT,
    keyword_coverage FLOAT,
    injected_keywords TEXT[],
    claude_reasoning TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Applications: one row per job applied to
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID REFERENCES jobs(id),
    profile_id UUID REFERENCES profiles(id),
    resume_variant_id UUID REFERENCES resume_variants(id),
    status VARCHAR(50) DEFAULT 'applied',
    ats_score FLOAT,
    applied_at TIMESTAMPTZ DEFAULT NOW(),
    last_status_at TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT,
    screenshot_path VARCHAR(500),
    error_log TEXT,
    is_auto_applied BOOLEAN DEFAULT FALSE,
    CONSTRAINT uq_application UNIQUE (job_id, profile_id)
);

CREATE INDEX IF NOT EXISTS ix_applications_status ON applications(status);

-- Email threads: classified career emails from Gmail
CREATE TABLE IF NOT EXISTS email_threads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID REFERENCES applications(id),
    gmail_thread_id VARCHAR(200) UNIQUE NOT NULL,
    gmail_message_id VARCHAR(200),
    subject VARCHAR(500),
    sender VARCHAR(300),
    snippet TEXT,
    classification VARCHAR(50) DEFAULT 'general',
    confidence FLOAT,
    received_at TIMESTAMPTZ,
    is_read BOOLEAN DEFAULT FALSE,
    is_notified BOOLEAN DEFAULT FALSE,
    raw_content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- In-app notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type VARCHAR(50) NOT NULL,
    title VARCHAR(300) NOT NULL,
    body TEXT,
    metadata JSONB DEFAULT '{}',
    is_read BOOLEAN DEFAULT FALSE,
    telegram_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Apply rate limiting logs
CREATE TABLE IF NOT EXISTS apply_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform VARCHAR(50) NOT NULL,
    date TIMESTAMPTZ DEFAULT NOW(),
    count INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS ix_apply_logs_platform_date ON apply_logs(platform, date);
