import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/',
});

api.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        if (error.response.status === 401) {
            console.log("prima");
            await api.get('/auth/refresh', {
                withCredentials: true,
            }).catch((error) => {
                console.log("401");
                localStorage.removeItem('user');
                localStorage.clear();
                console.log("40111111");
                window.location.href = '/';
                return Promise.reject(error);
            });

            return axios(error.config);
        }

        return Promise.reject(error);
    }
);

export default api;