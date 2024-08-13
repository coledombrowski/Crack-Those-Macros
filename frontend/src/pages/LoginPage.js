import React, { useState } from 'react';
import axiosInstance from 'axios'; // Path to axios configuration
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();

		try {
			const response = await axiosInstance.post('/login-user', {
				username,
				password,
			});

			console.log('Login successful:', response.data.message);
			navigate('/'); // Navigate to home page after successful login
		} catch (error) {
			console.error('Login failed:', error.response.data.message);
			setError(error.response.data.message);
		}
	};

	return (
		<div>
			<h2>Login</h2>
			<form onSubmit={handleSubmit}>
				<input
					type="text"
					placeholder="Username"
					value={username}
					onChange={(e) => setUsername(e.target.value)}
					required
				/>
				<br />
				<input
					type="password"
					placeholder="Password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
					required
				/>
				<br />
				<button type="submit">Login</button>
				{error && <p style={{ color: 'red' }}>{error}</p>}
			</form>
			<br></br>
			<br></br>
			New User? <button onClick={() => navigate('/createAccount')}>Create Account</button>
		</div>
	);
};

export default LoginPage;
