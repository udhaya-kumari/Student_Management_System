import { Link } from 'react-router-dom'

export default function StudentTable({ students, onDelete }) {
  if (!students || students.length === 0) {
    return <div className="empty-state">No Students Registered</div>
  }

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Student ID</th>
            <th>Register No</th>
            <th>Name</th>
            <th>Department</th>
            <th>Year</th>
            <th>Semester</th>
            <th>Section</th>
            <th>Phone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {students.map((s) => (
            <tr key={s.student_id}>
              <td>{s.student_id}</td>
              <td>{s.register_number}</td>
              <td>{s.first_name} {s.last_name}</td>
              <td>{s.department}</td>
              <td>{s.year}</td>
              <td>{s.semester}</td>
              <td>{s.section}</td>
              <td>{s.phone_number}</td>
              <td className="actions">
                <Link className="link-btn" to={`/students/${s.student_id}`}>View</Link>
                <Link className="link-btn" to={`/students/${s.student_id}/edit`}>Edit</Link>
                <button className="link-btn danger" onClick={() => onDelete(s)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
