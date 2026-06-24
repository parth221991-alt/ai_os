import { useState } from 'react'
import {
  LayoutDashboard, Briefcase, ClipboardList,
  UserCircle2, Mail, Zap,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import Dashboard from './pages/Dashboard'
import Jobs from './pages/Jobs'
import Applications from './pages/Applications'
import Profiles from './pages/Profiles'
import EmailInbox from './pages/EmailInbox'

type Page = 'dashboard' | 'jobs' | 'applications' | 'profiles' | 'email'

const NAV: { id: Page; label: string; Icon: React.FC<{ className?: string }> }[] = [
  { id: 'dashboard',    label: 'Dashboard',    Icon: LayoutDashboard },
  { id: 'jobs',         label: 'Jobs',         Icon: Briefcase },
  { id: 'applications', label: 'Applications', Icon: ClipboardList },
  { id: 'profiles',     label: 'Profiles',     Icon: UserCircle2 },
  { id: 'email',        label: 'Email',        Icon: Mail },
]

export default function App() {
  const [page, setPage] = useState<Page>('dashboard')

  const PAGES: Record<Page, React.ReactNode> = {
    dashboard:    <Dashboard />,
    jobs:         <Jobs />,
    applications: <Applications />,
    profiles:     <Profiles />,
    email:        <EmailInbox />,
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex">
      {/* Sidebar */}
      <nav className="w-56 shrink-0 bg-card border-r border-border flex flex-col">
        {/* Logo */}
        <div className="px-5 py-5 border-b border-border">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-md bg-indigo-600 flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <div>
              <p className="text-foreground font-bold text-sm font-chivo leading-none">CareerPilot</p>
              <p className="text-muted-foreground text-[10px] mt-0.5">Career OS</p>
            </div>
          </div>
        </div>

        {/* Nav */}
        <ul className="flex-1 py-3 space-y-0.5 px-2">
          {NAV.map(({ id, label, Icon }) => (
            <li key={id}>
              <button
                onClick={() => setPage(id)}
                className={cn(
                  'w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors',
                  page === id
                    ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-600/30'
                    : 'text-muted-foreground hover:text-foreground hover:bg-accent'
                )}
              >
                <Icon className="w-4 h-4 shrink-0" />
                {label}
              </button>
            </li>
          ))}
        </ul>

        {/* Footer */}
        <div className="px-5 py-4 border-t border-border">
          <p className="text-muted-foreground text-[10px]">v1.0.0 · Active</p>
        </div>
      </nav>

      {/* Main */}
      <main className="flex-1 overflow-auto">
        {PAGES[page]}
      </main>
    </div>
  )
}
