import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { studentApi } from '../services/api.js'
import ConfirmDialog from '../components/ConfirmDialog.jsx'

export default function StudentDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [student, setStudent] = useState(null)
  const [error, setError] = useState('')
  const [confirmOpen, setConfirmOpen] = useState(false)

  useEffect(() => {
    studentApi.get(id)
      .then((res) => setStudent(res.data.data))
      .catch(() => setError('Could not load student.'))
  }, [id])

  const handleDelete = () => {
    studentApi.remove(id).then(() => navigate('/students'))
  }

  if (error) return <div className="card"><p className="field-error">{error}</p></div>
  if (!student) return <div className="card"><p>Loading...</p></div>

  const rows = [
    ['Student ID', student.student_id],
    ['Register Number', student.register_number],
    ['First Name', student.first_name],
    ['Last Name', student.last_name],
    ['Date of Birth', student.date_of_birth],
    ['Gender', student.gender],
    ['Email', student.email],
    ['Phone Number', student.phone_number],
    ['Department', student.department],
    ['Year', student.year],
    ['Semester', student.semester],
    ['Section', student.section],
    ['Address', student.address || '-'],
    ['Parent/Guardian Phone', student.parent_phone_number],
  ]

  return (
    <div className="card">
      <div className="card-header">
        <h1>{student.first_name} {student.last_name}</h1>
        <div className="actions">
          <Link className="btn btn-secondary" to={`/students/${id}/edit`}>Edit</Link>
          <button className="btn btn-danger" onClick={() => setConfirmOpen(true)}>Delete</button>
        </div>
      </div>

      <dl className="detail-list">
        {rows.map(([label, value]) => (
          <div className="detail-row" key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>

      <Link className="btn btn-secondary" to="/students">Back to List</Link>

      <ConfirmDialog
        open={confirmOpen}
        title="Delete Student"
        message={`Are you sure you want to delete ${student.first_name} ${student.last_name}?`}
        onConfirm={handleDelete}
        onCancel={() => setConfirmOpen(false)}
      />
    </div>
  )
}
