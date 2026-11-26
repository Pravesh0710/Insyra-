import { useState } from "react";

const API_URL = "http://localhost:8000";

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [status, setStatus] = useState("");
  const [profile, setProfile] = useState(null);
  const [cleanResult, setCleanResult] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a file first.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading...");
    const res = await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    if (res.ok) {
      setFilename(data.filename);
      setStatus(`Uploaded: ${data.filename}`);
      setProfile(null);
      setCleanResult(null);
    } else {
      setStatus(data.detail || "Upload failed");
    }
  };

  const handleProfile = async () => {
    if (!filename) return;
    setStatus("Profiling...");
    const res = await fetch(`${API_URL}/profile/${filename}`);
    const data = await res.json();
    setProfile(data);
    setStatus("Profile ready!");
  };

  const handleClean = async () => {
    if (!filename) return;
    setStatus("Cleaning...");
    const res = await fetch(`${API_URL}/clean/${filename}`, {
      method: "POST",
    });
    const data = await res.json();
    setCleanResult(data);
    setStatus("Cleaning complete!");
  };

  return (
    <div style={{ maxWidth: "700px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Insyra</h1>
      <p>Upload a CSV or Excel file to profile and clean your data.</p>

      <div style={{ marginBottom: "16px" }}>
        <input
          type="file"
          accept=".csv,.xls,.xlsx"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={handleUpload} style={{ marginLeft: "8px" }}>
          Upload
        </button>
      </div>

      {status && <p><strong>Status:</strong> {status}</p>}

      {filename && (
        <div style={{ marginTop: "16px" }}>
          <button onClick={handleProfile}>Profile Data</button>
          <button onClick={handleClean} style={{ marginLeft: "8px" }}>
            Clean Data
          </button>
        </div>
      )}

      {profile && (
        <div style={{ marginTop: "24px" }}>
          <h3>Profile Report</h3>
          <pre style={{ background: "#f4f4f4", padding: "12px", overflowX: "auto" }}>
            {JSON.stringify(profile, null, 2)}
          </pre>
        </div>
      )}

      {cleanResult && (
        <div style={{ marginTop: "24px" }}>
          <h3>Clean Result</h3>
          <pre style={{ background: "#f4f4f4", padding: "12px", overflowX: "auto" }}>
            {JSON.stringify(cleanResult, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;