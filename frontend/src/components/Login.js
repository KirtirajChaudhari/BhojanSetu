import React, { useState } from 'react';
import { authService } from '../services/api';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await authService.login(username, password);
      onLogin(data.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const quickLogin = async (user, pass) => {
    setUsername(user);
    setPassword(pass);
    setError('');
    setLoading(true);
    try {
      const data = await authService.login(user, pass);
      onLogin(data.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">Hotel POS</h1>
        <p className="login-subtitle">Sign in to continue</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div style={{ marginTop: '24px', paddingTop: '24px', borderTop: '1px solid var(--border)' }}>
          <p style={{ textAlign: 'center', fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
            Quick Login:
          </p>
          <div style={{ display: 'grid', gap: '8px' }}>
            <button onClick={() => quickLogin('waiter1', 'waiter123')} className="btn btn-ghost btn-sm">
              Waiter
            </button>
            <button onClick={() => quickLogin('reception1', 'reception123')} className="btn btn-ghost btn-sm">
              Reception
            </button>
            <button onClick={() => quickLogin('chef1', 'chef123')} className="btn btn-ghost btn-sm">
              Chef / Kitchen
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
