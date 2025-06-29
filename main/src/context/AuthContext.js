import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const apiClient = axios.create({
  baseURL: "http://localhost:5000",
  withCredentials: true,
});

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        await apiClient.get('/api/check-auth');
        setIsAuthenticated(true);
      } catch (error) {
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };
    checkAuthStatus();
  }, []);

  const logout = async () => {
    try {
      await apiClient.get('/api/logout');
      setIsAuthenticated(false);
    } catch (error) {
      console.error("Błąd podczas wylogowywania", error);
    }
  };

  const value = { isAuthenticated, isLoading, logout };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};