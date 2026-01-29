import { createContext, useContext, useState, useEffect } from 'react'
import api from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('access_token'))
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadUser = async () => {
      const storedToken = localStorage.getItem('access_token')
      if (storedToken) {
        setToken(storedToken)
        try {
          const response = await api.get('/auth/user/')
          setUser(response.data)
        } catch (err) {
          console.error('Failed to load user:', err)
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          setToken(null)
        }
      }
      setLoading(false)
    }
    loadUser()
  }, [])

  const login = async (email, password) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/auth/login/', { email, password })
      const { access, refresh, user: userData } = response.data
      
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      setToken(access)
      setUser(userData)
      
      return { success: true }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message || 
                          'Login failed. Please check your credentials.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const register = async (data) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/auth/register/', data)
      return { success: true, data: response.data }
    } catch (err) {
      const errorMessage = err.response?.data?.email?.[0] || 
                          err.response?.data?.password?.[0] || 
                          err.response?.data?.detail || 
                          'Registration failed. Please try again.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setToken(null)
    setUser(null)
    setError(null)
  }

  const forgotPassword = async (email) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/auth/password-reset/', { email })
      return { success: true, message: response.data.message || 'Password reset email sent.' }
    } catch (err) {
      const errorMessage = err.response?.data?.email?.[0] || 
                          err.response?.data?.detail || 
                          'Failed to send password reset email.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const resetPassword = async (uid, token, password) => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.post('/auth/password-reset/confirm/', { 
        uid, 
        token, 
        password 
      })
      return { success: true, message: response.data.message || 'Password reset successfully.' }
    } catch (err) {
      const errorMessage = err.response?.data?.password?.[0] || 
                          err.response?.data?.token?.[0] || 
                          err.response?.data?.detail || 
                          'Failed to reset password.'
      setError(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      setLoading(false)
    }
  }

  const value = {
    user,
    token,
    loading,
    error,
    isAuthenticated: !!token,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
