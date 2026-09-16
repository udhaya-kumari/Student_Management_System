import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { studentApi } from '../services/api.js'
import StudentForm from '../components/StudentForm.jsx'

export default function EditStudent() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [student, setStudent] = useState(null)
  const [serverErrors, setServerErrors] = useState(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    studentApi.get(id)
      .then((res) => setStudent(res.data.data))
      .catch(() => setError('Could not load student.'))
  }, [id])

  const handleSubmit = (payload) => {
    setSubmitting(true)
    setServerErrors(null)
    studentApi.update(id, payload)
      .then(() => navigate(`/students/${id}`))
      .catch((err) => {
        setServerErrors(err.response?.data?.errors || { non_field_errors: ['Something went wrong.'] })
      })
      .finally(() => setSubmitting(false))
  }

  if (error) return <div className="card"><p className="field-error">{error}</p></div>
  if (!student) return <div className="card"><p>Loading...</p></div>

  return (
    <div className="card">
      <h1>Edit Student</h1>
      <StudentForm
        initialValues={student}
        onSubmit={handleSubmit}
        serverErrors={serverErrors}
        submitting={submitting}
        submitLabel="Save Changes"
      />
    </div>
  )
}
