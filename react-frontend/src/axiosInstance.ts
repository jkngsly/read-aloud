// src/axiosInstance.ts

import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000',  // Your backend base URL
  timeout: 10000,  // Optional: You can set a timeout if needed
});

export default axiosInstance;
