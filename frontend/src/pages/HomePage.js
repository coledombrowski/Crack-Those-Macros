import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from 'axios';
import '../css/HomePage.css'; 

const HomePage = () => {
  const navigate = useNavigate();
  const [loginData, setLoginData] = useState({
    isLoggedIn: "",
    username: "",
    goal: ""
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axiosInstance.get('/get-current-user-state');
      setLoginData({
        isLoggedIn: response.data.result,
        username: response.data?.username,
        goal: response.data?.goal
      });
    } catch (error) {
      console.error(error);
    }
  };

  const isLoggedIn = loginData.isLoggedIn === "True";
  const username = loginData.username || "User";

  // Display getMealSuggestion button if the user has an active goal set:
  if(loginData.goal) {
    return (
      <div>
        <h1>Crack-Those-Macros</h1>
        <img src="/Logo/220x250.png" alt="Crack-Those-Macros Logo" />
        {isLoggedIn ? (
          <div>
            <h2>Welcome, {username}!</h2>
            <button onClick={() => navigate('/questionnaire')}>Get started by sharing your fitness goals</button>
            <br /><br />
            <button onClick={() => navigate('/getMealSuggestion')}>Get a Meal!</button>
            <br /><br />
            <button onClick={() => navigate('/userDashboard')}>Fitness Profile</button>
          </div>
        ) : (
          <div>
            <h2>Create an Account</h2>
            <button onClick={() => navigate('/createAccount')}>Go to Create Account</button>
            <br /><br />
            <h2>Login</h2>
            <button onClick={() => navigate('/loginPage')}>Go to Login</button>
          </div>
        )}
      </div>
    );
  } else {
    // Hide the getMealSuggestion button
      return (
        <div>
          <h1>Crack-Those-Macros</h1>
          <img src="/Logo/220x250.png" alt="Crack-Those-Macros Logo" />
          {isLoggedIn ? (
            <div>
              <h2>Welcome, {username}!</h2>
              <button onClick={() => navigate('/questionnaire')}>Get started by sharing your fitness goals</button>
              <br /><br />
              <br /><br />
              <button onClick={() => navigate('/userDashboard')}>Fitness Profile</button>
            </div>
          ) : (
            <div>
              <h2>Create an Account</h2>
              <button onClick={() => navigate('/createAccount')}>Go to Create Account</button>
              <br /><br />
              <h2>Login</h2>
              <button onClick={() => navigate('/loginPage')}>Go to Login</button>
            </div>
          )}
        </div>
      );
  }
};

export default HomePage;
