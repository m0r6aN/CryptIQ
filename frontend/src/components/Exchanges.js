import { useState } from 'react';

const AddCEXAPIPage = () => {
  const [exchange, setExchange] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [message, setMessage] = useState('');

  const handleSave = async () => {
    if (!exchange || !apiKey || !apiSecret) {
      setMessage('Please fill all fields');
      return;
    }

    try {
      // Call your backend to save this API info securely
      const response = await fetch('/api/cex-apis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ exchange, apiKey, apiSecret })
      });

      if (response.ok) {
        setMessage('API info saved successfully!');
      } else {
        setMessage('Failed to save API info');
      }
    } catch (err) {
      console.error(err);
      setMessage('Error saving API info');
    }
  };

  return (
    <div>
      <h2>Add Centralized Exchange API Info</h2>
      <label>
        Select Exchange:
        <select value={exchange} onChange={(e) => setExchange(e.target.value)}>
          <option value="">Select Exchange</option>
          <option value="blofin">Blofin</option>
          <option value="crypto.com">Crypto.com</option>
          {/* Add more exchanges here */}
        </select>
      </label>
      <br />
      <label>
        API Key:
        <input
          type="text"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
      </label>
      <br />
      <label>
        API Secret:
        <input
          type="password"
          value={apiSecret}
          onChange={(e) => setApiSecret(e.target.value)}
        />
      </label>
      <br />
      <button onClick={handleSave}>Save API Info</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddCEXAPIPage;
