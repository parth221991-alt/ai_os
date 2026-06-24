import { type VariantProps, cva } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary/20 text-primary border border-primary/30',
        secondary: 'bg-secondary text-secondary-foreground border border-border',
        destructive: 'bg-destructive/20 text-red-400 border border-red-900/40',
        success: 'bg-emerald-950/60 text-emerald-400 border border-emerald-900/40',
        warning: 'bg-amber-950/60 text-amber-400 border border-amber-900/40',
        info: 'bg-sky-950/60 text-sky-400 border border-sky-900/40',
        outline: 'border border-border text-muted-foreground',
      },
    },
    defaultVariants: { variant: 'default' },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}
