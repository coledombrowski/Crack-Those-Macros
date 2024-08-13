import React, { useState } from 'react';
import axiosInstance from 'axios';
import { useNavigate } from 'react-router-dom';


const CreateAccount = () => {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		e.preventDefault();

		try {
			const response = await axiosInstance.post('/register-account', {
				username,
				password,
			});
			console.log(response.data.message);
			navigate('/loginPage');// Navigate to login page after successful account creation
		} catch (error) {
			console.error(error.response.data.message);
			setError(error.response.data.message);
		}
	};

	return (
		<div>
			<h2>Create Account</h2>
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
				<button type="submit">Create Account</button>
				{error && <p style={{ color: 'red' }}>{error}</p>}
			</form>
			<br></br>
			<br></br>
			Already have an account? <button onClick={() => navigate('/loginPage')}>Login</button>
		</div>
	);
};

export default CreateAccount;

