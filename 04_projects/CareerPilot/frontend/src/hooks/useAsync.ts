import { useCallback, useEffect, useRef, useState } from 'react'

interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export function useAsync<T>(
  fn: () => Promise<T>,
  deps: React.DependencyList = []
): AsyncState<T> & { reload: () => void } {
  const [state, setState] = useState<AsyncState<T>>({ data: null, loading: true, error: null })
  const mountedRef = useRef(true)

  const run = useCallback(async () => {
    setState(s => ({ ...s, loading: true, error: null }))
    try {
      const data = await fn()
      if (mountedRef.current) setState({ data, loading: false, error: null })
    } catch (e) {
      if (mountedRef.current) setState({ data: null, loading: false, error: (e as Error).message })
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  useEffect(() => {
    mountedRef.current = true
    run()
    return () => { mountedRef.current = false }
  }, [run])

  return { ...state, reload: run }
}
