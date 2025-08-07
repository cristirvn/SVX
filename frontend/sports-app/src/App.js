import React, { useState } from 'react';
import api from './api.js'; // Axios instance for API calls

const App = () => {
  // State variables
  const [country, setCountry] = useState('');
  const [sport, setSport] = useState('');
  const [leagues, setLeagues] = useState([]);
  const [error, setError] = useState('');

  // Handle form submission
  const fetchLeagues = async (event) => {
    event.preventDefault(); // Prevent page reload
    setError(''); // Clear previous errors
    setLeagues([]); // Clear previous results

    try {
      // API call
      console.log(`Fetching leagues for sport=${sport} and country=${country}`);
      const response = await api.get(`/leagues/?sport=${sport}&country=${country}`);
      console.log('API response:', response.data); // Debugging
      setLeagues(response.data); // Update leagues state
    } catch (err) {
      if (err.response) {
        // Handle API errors
        setError(err.response.data.detail || 'An error occurred.');
      } else {
        // Handle network or unexpected errors
        setError('Failed to fetch leagues. Please try again.');
      }
    }
  };

  return (
    <div style={{ margin: '2rem' }}>
      <h1 className='h1'>Leagues Finder</h1>
      <form className ='form' onSubmit={fetchLeagues}>
        <div>
          <label className='label'>Country:</label>
          <input
            className='input'
            type="text"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            required
          />
        </div>
        <div>
          <label className='label'>Sport:</label>
          <input
            className='input'
            type="text"
            value={sport}
            onChange={(e) => setSport(e.target.value)}
            required
          />
        </div>
        <button className='button' type="submit">Fetch Leagues</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {leagues.length > 0 && (
        <div className='output'>
          <h2 >List of leagues bellow:</h2>
          <ul className='ul'>
            {leagues.map((league, index) => (
              <ol className ='li' key={index}>{league}</ol>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default App;
