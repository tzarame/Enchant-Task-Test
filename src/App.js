import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://app:8000/api/test')
      .then(response => {
        if (!response.ok) { throw new Error(`HTTP error! status: ${response.status}`); }
        return response.json();
      })
      .then(data => setData(data))
      .catch(error => setError(error.toString()));
  }, []);

  return (
    <div>
      <h1>Hello, React!</h1>
      <p>The application is running and working сука блядь.</p>
      {error && <p>Error: {error}</p>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}

export default App;