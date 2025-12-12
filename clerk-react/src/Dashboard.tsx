import React, { useState } from 'react';

export default function Dashboard() {
  // Example dashboard info
  const [dashboardInfo, setDashboardInfo] = useState({
    title: 'My Dashboard',
    notes: '',
    tasks: '',
  });

  return (
    <div style={{ padding: 24, width: '100%', height: '100%', boxSizing: 'border-box' }}>
      <h2>{dashboardInfo.title}</h2>
      <div>
        <label>Notes:</label>
        <textarea
          value={dashboardInfo.notes}
          onChange={e => setDashboardInfo({ ...dashboardInfo, notes: e.target.value })}
          rows={4}
          style={{ width: '100%' }}
        />
      </div>
      <div>
        <label>Tasks:</label>
        <input
          type="text"
          value={dashboardInfo.tasks}
          onChange={e => setDashboardInfo({ ...dashboardInfo, tasks: e.target.value })}
        />
      </div>
    </div>
  );
}
