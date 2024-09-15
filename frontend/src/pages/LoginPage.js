import React, { useState } from 'react';
import { login } from '../services/auth';

function LoginPage({ history }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await login(email, password);
      history.push('/portfolio');
    } catch (error) {
      console.error('Login failed:', error);
      // Handle error (display message to user)
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-xl mb-4">Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-2">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            className="w-full p-2"
          />
        </div>
        <div className="mb-2">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="w-full p-2"
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white p-2">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;
