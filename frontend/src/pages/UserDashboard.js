import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from 'axios';
import '../css/UserDashboard.css';

const UserDashboard = () => {
	const navigate = useNavigate();
	const [userProfileData, setUserProfileData] = useState({
		name: "",
		heightFeet: "",
		heightInches: "",
		weight: "",
		goal: ""
	});
	
	useEffect(() => {
		fetchData();
	}, []);
	const fetchData = async () => {
		try {
			const response = await axiosInstance.get('/api/get-user-profile');
			setUserProfileData({
				name: response.data.userProfileData.name,
				heightFeet: response.data.userProfileData.heightFeet,
				heightInches: response.data.userProfileData.heightInches,
				weight: response.data.userProfileData.weight,
				goal: response.data.userProfileData?.goal,
			});
		} catch (error) {
			console.error(error);
		}
	};

	// Display getMealSuggestion button if the user has an active goal set:
	if(userProfileData.goal) {
		return (
			<div className="dashboard-container">
				<h2 className="dashboard-title">User Dashboard</h2>
				<table className='display-table'>
					<tr>
						<th>Name</th>
						<th>Height</th>
						<th>Weight</th>
						<th>Current Goal</th>
					</tr>
					<tr>
						<td>{userProfileData.name}</td>
						<td>{userProfileData.heightFeet} ft {userProfileData.heightInches} in</td>
						<td>{userProfileData.weight}</td>
						<td>{userProfileData.goal}</td>
					</tr>
				</table>
				<br></br><br></br>
				<h3>Looking good?</h3>
				<button onClick={() => navigate('/getMealSuggestion')}>Let's get a Meal!</button>
				<br></br><br></br>
				<br></br><br></br>
				<h3>Need to update your profile information?</h3>
				<button onClick={() => navigate('/questionnaire')}>Revisit the Questionnaire</button>
			</div>
		);
	} else {
		// Hide the getMealSuggestion button
		return (
			<div className="dashboard-container">
				<h2 className="dashboard-title">User Dashboard</h2>
				<table className='display-table'>
					<tr>
						<th>Name</th>
						<th>Height</th>
						<th>Weight</th>
						<th>Current Goal</th>
					</tr>
					<tr>
						<td>{userProfileData.name}</td>
						<td>{userProfileData.heightFeet} ft {userProfileData.heightInches} in</td>
						<td>{userProfileData.weight}</td>
						<td>{userProfileData.goal}</td>
					</tr>
				</table>
				<br></br><br></br>
				<br></br><br></br>
				<br></br><br></br>
				<h3>Need to update your profile information?</h3>
				<button onClick={() => navigate('/questionnaire')}>Revisit the Questionnaire</button>
			</div>
		);
	}
	
};

export default UserDashboard;
