import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor untuk menambahkan token ke header request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor untuk handle token expired dan auto-refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Cek jika error karena token expired (401 Unauthorized)
    if (
      error.response?.status === 401 &&
      error.response.data?.code === 'token_not_valid' &&
      error.response.data?.messages?.[0]?.token_class === 'AccessToken' &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true; // Flag untuk menghindari infinite loop
      const refreshToken = localStorage.getItem('refresh_token');

      if (!refreshToken) {
        // Jika tidak ada refresh token, logout
        localStorage.removeItem('token');
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        // Request token baru menggunakan refresh token
        const { data } = await api.post('accounts/token/refresh/', {
          refresh: refreshToken,
        });

        // Simpan token baru
        const newAccessToken = data.access;
        localStorage.setItem('token', newAccessToken);

        // Update header request dengan token baru
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

    
        return api(originalRequest);
      } catch (refreshError) {
     
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    // Jika error bukan karena token expired, reject biasa
    return Promise.reject(error);
  }
);

export default api;