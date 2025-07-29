import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";

function Dashboard() {
  const [status, setStatus] = useState("");

  useEffect(() => {
    fetch("https://leviathan-1.onrender.com/")
      .then((res) => res.text())
      .then((data) => setStatus(data));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Leviathan Dashboard</h1>
      <p className="mb-4">Backend status: {status}</p>
      <Link className="text-blue-500 underline" to="/leads">View Leads</Link>
    </div>
  );
}

function Leads() {
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    fetch("https://leviathan-1.onrender.com/api/leads")
      .then((res) => res.json())
      .then((data) => setLeads(data));
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-2">Captured Leads</h2>
      <ul>
        {leads.map((lead, index) => (
          <li key={index} className="border p-2 mb-2 rounded">
            <p><strong>Email:</strong> {lead.email}</p>
            <p><strong>Product:</strong> {lead.product}</p>
            <p><strong>Timestamp:</strong> {lead.timestamp}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

function App() {
  return (
    <Router>
      <nav className="bg-gray-800 p-4 text-white">
        <Link className="mr-4" to="/">Dashboard</Link>
        <Link to="/leads">Leads</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/leads" element={<Leads />} />
      </Routes>
    </Router>
  );
}

export default App;
