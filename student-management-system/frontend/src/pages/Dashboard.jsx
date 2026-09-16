import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { studentApi } from '../services/api.js'

export default function Dashboard() {
  const [count, setCount] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    studentApi.list()
      .then((res) => setCount(res.data.data.length))
      .catch(() => setError('Could not reach the backend API.'))
  }, [])

  return (
    <div className="card">
      
      <p>Welcome to the Student Management System.</p>
      {error && <p className="field-error">{error}</p>}
      <div className="stat-box">
        <div className="stat-number">{count ?? '-'}</div>
        <div className="stat-label">Total Students</div>
      </div>
      <Link className="btn btn-primary" to="/students">Go to Student List</Link>
    </div>
  )
}
