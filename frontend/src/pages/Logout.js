import React, { useState, useEffect } from 'react';
import axiosInstance from 'axios';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
    const [result, setResult] = useState({
        result: "",
        message: "",
    });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await axiosInstance.get('/logout-user');
            setResult({
                result: response.data.result,
                message: response.data.message
            });
            console.log('Logout successful:', response.data.message);
        } catch (error) {
            console.error('Logout failed:', error.response.data.message);
            setError(error.response.data.message);
        }
    };

    return (
        <div>
            <h2>{result.result}</h2>
            <h3>{result.message}</h3>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button onClick={() => navigate('/')}>Return to Home</button>
        </div>
    );
};

export default Logout;
