import { useEffect } from 'react'
import { Outlet, useLocation } from 'react-router'
import { Navbar } from './Navbar'
import { Footer } from './Footer'
import { InteractiveGrid } from './InteractiveGrid'

export function Layout() {
  const { pathname } = useLocation()

  // A client-side route change leaves the scroll position where it was, which
  // lands you halfway down a page you have not read yet.
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <>
      <InteractiveGrid />
      <div className="layout">
        <Navbar />
        <main className="main-content">
          <Outlet />
        </main>
        <Footer />
      </div>
    </>
  )
}
