import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from 'axios';
import '../css/Meal-Suggestion.css';

const GetMealSuggestionPage = () => {
    const navigate = useNavigate();
    const [goal, setGoal] = useState('');
    const [mealTimeChoice, setMealTimeChoice] = useState('');

    useEffect(() => {
        fetchData();
    }, []);
    const fetchData = async () => {
        try {
            const response = await axiosInstance.get('/api/get-user-goals');
            setGoal(response.data.goal);
        } catch (error) {
            console.error(error);
        }
    };

    async function handleSubmitWeightSuggestion(e) {
        e.preventDefault();
        try {
            let mealResponse = await axiosInstance.post('/api/get-meal-suggestion', {
                mealTimeChoice
            });
            console.log(mealResponse.data.recommendation.meal);
            console.log("Meal data being sent:", mealResponse.data.recommendation.meal);
            navigate('/meal-suggestion-result', {state: {meal: mealResponse.data.recommendation.meal}});

        } catch (error) {
            console.error(error);
        }
    }

    async function handleSubmitProteinSuggestion(e) {
        e.preventDefault();
        try {
            let mealResponse = await axiosInstance.post('/api/get-meal-suggestion/protein', {
                mealTimeChoice
            });
            console.log(mealResponse.data.recommendation.meal);
            console.log(mealResponse.data.recommendation.message);
            console.log("Meal data being sent:", mealResponse.data.recommendation.meal);
            navigate('/meal-suggestion-result', {state: {meal: mealResponse.data.recommendation.meal}});

        } catch (error) {
            console.error(error);
        }
    }

    if (goal.toLowerCase().includes("weight")) {
        // Display components to fetch a weight loss recommendation
        return (
            <div className="meal-suggestion-page">
                <h2>Meal Suggestions</h2>
                <form onSubmit={handleSubmitWeightSuggestion}>
                    <div className="form-group">
                        <label>Meal Time:</label>
                        <select value={mealTimeChoice} onChange={(e) => setMealTimeChoice(e.target.value)}>
                            <option value="">Select</option>
                            <option value="Breakfast">Breakfast</option>
                            <option value="Lunch">Lunch</option>
                            <option value="Dinner">Dinner</option>
                        </select>
                    </div>
                    <button type="submit">Get a meal suggestion!</button>
                </form>
            </div>
        );
    } else {
        // Display components to fetch a protein recommendation
        return (
            <div className="meal-suggestion-page">
                <h2>Meal Suggestions</h2>
                <form onSubmit={handleSubmitProteinSuggestion}>
                    <div className="form-group">
                        <label>Meal Time:</label>
                        <select value={mealTimeChoice} onChange={(e) => setMealTimeChoice(e.target.value)}>
                            <option value="">Select</option>
                            <option value="Breakfast">Breakfast</option>
                            <option value="Lunch">Lunch</option>
                            <option value="Dinner">Dinner</option>
                        </select>
                    </div>
                    <button type="submit">Get a high protein meal!</button>
                </form>
            </div>
        );
    }
};

export default GetMealSuggestionPage;
