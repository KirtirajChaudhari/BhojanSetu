import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import WaiterPortal from './components/WaiterPortal';
import ReceptionPortal from './components/ReceptionPortal';
import KitchenPortal from './components/KitchenPortal';
import { authService } from './services/api';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const savedUser = authService.getUser();
    if (savedUser && authService.isAuthenticated()) {
      setUser(savedUser);
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = async () => {
    await authService.logout();
    setUser(null);
  };

  if (loading) {
    return (
      <div className="loading">
        <div>Loading...</div>
      </div>
    );
  }

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  const renderPortal = () => {
    switch (user.role) {
      case 'waiter':
        return <WaiterPortal user={user} />;
      case 'reception':
        return <ReceptionPortal user={user} />;
      case 'chef':
        return <KitchenPortal user={user} />;
      default:
        return <WaiterPortal user={user} />;
    }
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>🍽️ Hotel POS System</h1>
        <div className="header-user">
          <div className="user-info">
            <span className="user-name">{user.username}</span>
            <div className="user-role">{user.role}</div>
          </div>
          <button onClick={handleLogout} className="btn btn-danger btn-sm">
            Logout
          </button>
        </div>
      </header>
      <main className="app-main">{renderPortal()}</main>
    </div>
  );
}
