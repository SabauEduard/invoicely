'use client';

import { createContext, use, useState, useContext, useEffect } from "react";
import api from "../api/api";

const AuthContext = createContext({});
const LOGIN_URL = '/auth/login';
const ME_URL = '/auth/current-user';

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const user = localStorage.getItem('user');
        if (user) {
            setUser(JSON.parse(user));
        }
    }, []);

    const loginApiCall = async (payload) => {
        try {
            const response = await api.post(LOGIN_URL, payload,
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    withCredentials: true,
                });
            const token = response.data.access_token;

            const user_response = await api.get(ME_URL,
                {
                    withCredentials: true,
                });

            setUser(user_response.data);
            localStorage.setItem('user', JSON.stringify(user_response.data));
            return response.status;
        } catch (error) {
            throw error;
        }
    }

    const logout = async () => {
        document.cookie = "auth_cookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        localStorage.removeItem('user');
        localStorage.clear();
        setUser(null);
    }

    return (
        <AuthContext.Provider value={{ loginApiCall, logout, user }}>
            {children}
        </AuthContext.Provider>
    )
};

export default AuthContext;

export const useAuth = () => useContext(AuthContext);