import { useEffect, useState, useCallback } from 'react'
import { Link } from 'react-router-dom'
import { studentApi } from '../services/api.js'
import StudentTable from '../components/StudentTable.jsx'
import SearchBar from '../components/SearchBar.jsx'
import ConfirmDialog from '../components/ConfirmDialog.jsx'

export default function StudentList() {
  const [students, setStudents] = useState([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [toDelete, setToDelete] = useState(null)

  const fetchStudents = useCallback((searchValue) => {
    setLoading(true)
    studentApi.list(searchValue ? { search: searchValue } : {})
      .then((res) => {
        setStudents(res.data.data)
        setError('')
      })
      .catch(() => setError('Failed to load students.'))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => fetchStudents(search), 300)
    return () => clearTimeout(timer)
  }, [search, fetchStudents])

  const confirmDelete = () => {
    studentApi.remove(toDelete.student_id)
      .then(() => {
        setToDelete(null)
        fetchStudents(search)
      })
      .catch(() => {
        setError('Failed to delete student.')
        setToDelete(null)
      })
  }

  return (
    <div className="card">
      <div className="card-header">
        <h1>Manage Students</h1>
        <Link className="btn btn-primary" to="/students/add">+ Add New Student</Link>
      </div>

      <SearchBar value={search} onChange={setSearch} placeholder="Search by name, register no. or email" />

      {error && <p className="field-error">{error}</p>}
      {loading ? <p>Loading...</p> : (
        <StudentTable students={students} onDelete={setToDelete} />
      )}

      <ConfirmDialog
        open={!!toDelete}
        title="Delete Student"
        message={toDelete ? `Are you sure you want to delete ${toDelete.first_name} ${toDelete.last_name}?` : ''}
        onConfirm={confirmDelete}
        onCancel={() => setToDelete(null)}
      />
    </div>
  )
}
