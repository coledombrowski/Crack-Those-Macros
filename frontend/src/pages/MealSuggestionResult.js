import React from 'react';
import {useNavigate } from 'react-router-dom';
import '../css/Meal-Suggestion.css';
import { useLocation } from 'react-router-dom';

const MealSuggestionResult = () => {
    const location = useLocation();
    const meal = location.state.meal;

    console.log("Received meal data in component:", meal);

    return (
        <div className="meal-suggestion-result">
            <h1>Meal Suggestion</h1>
            <div className="meal-details">
                <p>Store: {meal?.store}</p>
                <p>Name: {meal?.name}</p>
                <p>Serving Size: {meal?.servingSize} {meal?.servingSizeType}</p>
                <p>Calories: {meal?.calories}</p>
                <p>Total Fat: {meal?.totalFat} g</p>
                <p>Cholesterol: {meal?.cholesterol} mg</p>
                <p>Sodium: {meal?.sodium} mg</p>
                <p>Total Carbohydrates: {meal?.totalCarbohydrate} g</p>
                <p>Fiber: {meal?.fiber} g</p>
                <p>Sugars: {meal?.sugars} g</p>
                <p>Protein: {meal?.protein} g</p>
                <p>Store: {meal?.store}</p>
            </div>
            <button onClick={() => window.history.back()}>Go Back</button>
        </div>
    );
};

export default MealSuggestionResult;