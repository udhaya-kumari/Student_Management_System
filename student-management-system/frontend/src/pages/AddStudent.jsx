import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { studentApi } from '../services/api.js'
import StudentForm from '../components/StudentForm.jsx'

export default function AddStudent() {
  const navigate = useNavigate()
  const [serverErrors, setServerErrors] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = (payload) => {
    setSubmitting(true)
    setServerErrors(null)
    studentApi.create(payload)
      .then(() => navigate('/students'))
      .catch((err) => {
        setServerErrors(err.response?.data?.errors || { non_field_errors: ['Something went wrong.'] })
      })
      .finally(() => setSubmitting(false))
  }

  return (
    <div className="card">
      <h1>Add Student</h1>
      <StudentForm onSubmit={handleSubmit} serverErrors={serverErrors} submitting={submitting} submitLabel="Add Student" />
    </div>
  )
}
