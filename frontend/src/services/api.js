// API configuration and helpers
const API_BASE = '/api';

// Auth functions
export const authService = {
  async login(username, password) {
    const response = await fetch(`${API_BASE}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Login failed');
    }

    const data = await response.json();
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  },

  async logout() {
    const token = localStorage.getItem('token');
    if (token) {
      await fetch(`${API_BASE}/auth/logout/`, {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
    }
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  getToken() {
    return localStorage.getItem('token');
  },

  isAuthenticated() {
    return !!this.getToken();
  },
};

// API helpers with authentication
export const api = {
  async get(url) {
    const response = await fetch(`${API_BASE}${url}`, {
      headers: {
        'Authorization': `Token ${authService.getToken()}`,
      },
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.error || 'Request failed');
    }
    return response.json();
  },

  async post(url, data) {
    const response = await fetch(`${API_BASE}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${authService.getToken()}`,
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || error.error || JSON.stringify(error));
    }
    return response.json();
  },
};
