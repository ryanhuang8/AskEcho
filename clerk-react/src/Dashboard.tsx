import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [dashboardInfo, setDashboardInfo] = useState({
    title: 'My Dashboard',
    notes: '',
    tasks: '',
  });
  
  const VIDEO_ID = 'video_693b73d67e288190a8462fd30ab410ed08ffe349861ceeba';

  return (
    <div style={{ padding: 24, width: '100%', height: '100%', boxSizing: 'border-box', maxWidth: 1200, margin: '0 auto' }}>
      <h2>{dashboardInfo.title}</h2>
      
      {/* Video Section */}
      <div style={{ marginBottom: 24, background: '#f5f5f5', padding: 16, borderRadius: 8 }}>
        <h3 style={{ marginTop: 0 }}>Sora Video</h3>
        <video 
          controls 
          style={{ width: '100%', maxWidth: 800, borderRadius: 8 }}
          src="/video.mp4"
        >
          Your browser does not support the video tag.
        </video>
        <p style={{ fontSize: 12, color: '#666', marginTop: 8 }}>
          Video ID: {VIDEO_ID}
        </p>
      </div>

      {/* Notes Section */}
      <div style={{ marginBottom: 16 }}>
        <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Notes:</label>
        <textarea
          value={dashboardInfo.notes}
          onChange={e => setDashboardInfo({ ...dashboardInfo, notes: e.target.value })}
          rows={4}
          style={{ width: '100%', padding: 8, borderRadius: 4, border: '1px solid #ccc' }}
          placeholder="Add your notes here..."
        />
      </div>

      {/* Tasks Section */}
      <div>
        <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>Tasks:</label>
        <input
          type="text"
          value={dashboardInfo.tasks}
          onChange={e => setDashboardInfo({ ...dashboardInfo, tasks: e.target.value })}
          style={{ width: '100%', padding: 8, borderRadius: 4, border: '1px solid #ccc' }}
          placeholder="Add a task..."
        />
      </div>
    </div>
  );
}