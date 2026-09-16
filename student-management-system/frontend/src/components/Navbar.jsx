import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const { pathname } = useLocation()
  const isActive = (path) => pathname === path || (path !== '/' && pathname.startsWith(path))

  return (
    <header className="navbar">
      <Link to="/" className="brand">STUDENT MANAGMENT SYSTEM</Link>
      <nav className="nav-links">
        <Link className={isActive('/') && pathname === '/' ? 'active' : ''} to="/">Dashboard</Link>
        <Link className={isActive('/students') ? 'active' : ''} to="/students">Students</Link>
      </nav>
    </header>
  )
}
