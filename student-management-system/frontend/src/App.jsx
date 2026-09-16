import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Dashboard from './pages/Dashboard.jsx'
import StudentList from './pages/StudentList.jsx'
import AddStudent from './pages/AddStudent.jsx'
import EditStudent from './pages/EditStudent.jsx'
import StudentDetails from './pages/StudentDetails.jsx'

export default function App() {
  return (
    <div className="app">
      <Navbar />
      <main className="page-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/students" element={<StudentList />} />
          <Route path="/students/add" element={<AddStudent />} />
          <Route path="/students/:id" element={<StudentDetails />} />
          <Route path="/students/:id/edit" element={<EditStudent />} />
        </Routes>
      </main>
    </div>
  )
}
