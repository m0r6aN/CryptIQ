import API from './api';

export const login = async (email, password) => {
  const response = await API.post('accounts/token/', { email, password });
  localStorage.setItem('access_token', response.data.access);
  localStorage.setItem('refresh_token', response.data.refresh);
  API.defaults.headers.Authorization = `Bearer ${response.data.access}`;
  return response;
};

export const register = async (email, password, pin) => {
  const response = await API.post('accounts/register/', { email, password, pin });
  return response;
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  delete API.defaults.headers.Authorization;
};
