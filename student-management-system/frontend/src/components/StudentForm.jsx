import { useState, useEffect } from 'react'

const emptyForm = {
  register_number: '',
  first_name: '',
  last_name: '',
  date_of_birth: '',
  gender: '',
  email: '',
  phone_number: '',
  department: '',
  year: '',
  semester: '',
  section: '',
  address: '',
  parent_phone_number: '',
}

// Shared by AddStudent and EditStudent. `initialValues` pre-fills the
// form for edit mode; `serverErrors` renders field-level messages
// returned by the Django API (e.g. duplicate register number).
export default function StudentForm({ initialValues, serverErrors, submitting, onSubmit, submitLabel }) {
  const [form, setForm] = useState(emptyForm)
  const [clientErrors, setClientErrors] = useState({})

  useEffect(() => {
    if (initialValues) setForm({ ...emptyForm, ...initialValues })
  }, [initialValues])

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const validate = () => {
    const errors = {}
    const required = [
      'register_number', 'first_name', 'last_name', 'date_of_birth', 'gender',
      'email', 'phone_number', 'department', 'year', 'semester', 'section',
      'parent_phone_number',
    ]
    required.forEach((field) => {
      if (!String(form[field] ?? '').trim()) errors[field] = 'This field is required.'
    })
    if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      errors.email = 'Enter a valid email address.'
    }
    if (form.phone_number && !/^\+?\d{7,15}$/.test(form.phone_number)) {
      errors.phone_number = 'Enter a valid phone number.'
    }
    if (form.parent_phone_number && !/^\+?\d{7,15}$/.test(form.parent_phone_number)) {
      errors.parent_phone_number = 'Enter a valid phone number.'
    }
    setClientErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!validate()) return
    onSubmit({ ...form, year: Number(form.year), semester: Number(form.semester) })
  }

  const errorFor = (field) => clientErrors[field] || (serverErrors && serverErrors[field]?.[0])

  return (
    <form className="student-form" onSubmit={handleSubmit} noValidate>
      <div className="form-grid">
        <Field label="Register Number" name="register_number" value={form.register_number} onChange={handleChange} error={errorFor('register_number')} />
        <Field label="First Name" name="first_name" value={form.first_name} onChange={handleChange} error={errorFor('first_name')} />
        <Field label="Last Name" name="last_name" value={form.last_name} onChange={handleChange} error={errorFor('last_name')} />
        <Field label="Date of Birth" name="date_of_birth" type="date" value={form.date_of_birth} onChange={handleChange} error={errorFor('date_of_birth')} />

        <div className="field">
          <label>Gender</label>
          <select name="gender" value={form.gender} onChange={handleChange}>
            <option value="">Select</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
          {errorFor('gender') && <span className="field-error">{errorFor('gender')}</span>}
        </div>

        <Field label="Email" name="email" type="email" value={form.email} onChange={handleChange} error={errorFor('email')} />
        <Field label="Phone Number" name="phone_number" value={form.phone_number} onChange={handleChange} error={errorFor('phone_number')} />
        <Field label="Department" name="department" value={form.department} onChange={handleChange} error={errorFor('department')} />
        <Field label="Year" name="year" type="number" value={form.year} onChange={handleChange} error={errorFor('year')} />
        <Field label="Semester" name="semester" type="number" value={form.semester} onChange={handleChange} error={errorFor('semester')} />
        <Field label="Section" name="section" value={form.section} onChange={handleChange} error={errorFor('section')} />
        <Field label="Parent/Guardian Phone" name="parent_phone_number" value={form.parent_phone_number} onChange={handleChange} error={errorFor('parent_phone_number')} />

        <div className="field field-wide">
          <label>Address (optional)</label>
          <textarea name="address" value={form.address || ''} onChange={handleChange} rows={2} />
        </div>
      </div>

      {serverErrors?.non_field_errors && (
        <p className="field-error">{serverErrors.non_field_errors[0]}</p>
      )}

      <button className="btn btn-primary" type="submit" disabled={submitting}>
        {submitting ? 'Saving...' : submitLabel || 'Save'}
      </button>
    </form>
  )
}

function Field({ label, name, value, onChange, type = 'text', error }) {
  return (
    <div className="field">
      <label>{label}</label>
      <input type={type} name={name} value={value} onChange={onChange} />
      {error && <span className="field-error">{error}</span>}
    </div>
  )
}
