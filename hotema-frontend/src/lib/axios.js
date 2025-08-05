import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor: Tambahkan token ke header
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: Handle expired token dan refresh otomatis
api.interceptors.response.use(
  (response) => response, // Jika sukses, langsung kembalikan response
  async (error) => {
    const originalRequest = error.config

    // Cek apakah error karena access token expired
    if (
      error.response?.status === 401 &&
      error.response.data?.code === 'token_not_valid' &&
      error.response.data?.messages?.[0]?.token_class === 'AccessToken' &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          // Minta access token baru
          const res = await axios.post('http://localhost:8000/api/token/refresh/', {
            refresh: refreshToken,
          })

          const newAccessToken = res.data.access
          localStorage.setItem('token', newAccessToken)

          // Update Authorization header dengan token baru
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
          return api(originalRequest) // Ulangi request sebelumnya
        } catch (refreshError) {
          // Refresh token juga tidak valid
          localStorage.removeItem('token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login' // Redirect ke halaman login
        }
      } else {
        // Tidak ada refresh token, langsung redirect
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api
