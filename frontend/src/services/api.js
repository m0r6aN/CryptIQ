import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

// Add a request interceptor to include the token in headers if available
API.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

export default API;
