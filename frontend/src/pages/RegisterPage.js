import { useState } from 'react';

const RegisterPage = () => {
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');

  const handleRegister = () => {
    if (pin.length !== 6 || isNaN(pin)) {
      setError('PIN must be exactly 6 digits');
      return;
    }
    // Here, you'd send the PIN to your backend for registration
    // Example:
    // fetch('/api/register', { method: 'POST', body: JSON.stringify({ pin }) })

    setError('');
    alert('Registered successfully');
  };

  return (
    <div>
      <h2>Register</h2>
      <input
        type="password"
        maxLength="6"
        placeholder="Enter 6-digit PIN"
        value={pin}
        onChange={(e) => setPin(e.target.value)}
      />
      <button onClick={handleRegister}>Register</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default RegisterPage;
