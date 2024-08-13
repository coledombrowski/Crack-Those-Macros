import random
import pyodbc
import pandas as pd
from addMeal import upsert_questionnaire_results
from proteinIntakeAlgorithm import get_protein_recommendation

server = 'crackthosemacros.database.windows.net'
database = 'crackthosemacros'
username = 'Admin_Shared'
password = 'ZeroCalories!0'
driver = '{SQL Server}'  # Adjust driver as needed
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_recommendation_object(recommendation):
    recommendation_object = {
        "foodId": str(recommendation['food_id']),
        "store": recommendation['Store'],
        "name": recommendation['Name'],
        "servingSize": recommendation['SERVING_SIZE'],
        "servingSizeType": recommendation['SERVING_SIZE_TYPE'],
        "calories": recommendation['CALORIES'],
        "totalFat": recommendation['TOTAL_FAT'],
        "cholesterol": recommendation['CHOLESTEROL'],
        "sodium": recommendation['SODIUM'],
        "totalCarbohydrate": recommendation['TOTAL_CARBOHYDRATE'],
        "fiber": recommendation['FIBER'],
        "sugars": recommendation['SUGARS'],
        "protein": recommendation['PROTEIN']
    }
    return recommendation_object

def get_calories(goal, amount, pounds, weight,meal_time):
    # Base calories based on weight category
    base_calories = {
        "0-99 lb": 1400,
        "100-150 lb": 1800,
        "151-200 lb": 2200,
        "201-250 lb": 2600,
        "251-300 lb": 3000
    }

    # Adjust calories based on goal and amount
    calorie_adjustment = 0
    if goal == "Gain weight":
        if pounds == 15:
            calorie_adjustment = 600 if amount == "A little weight" else 800
        elif pounds == 20:
            calorie_adjustment = 700 if amount == "A little weight" else 900
    elif goal == "Lose weight":
        if pounds == 5:
            calorie_adjustment = -400 if amount == "A little weight" else -600
        elif pounds == 10:
            calorie_adjustment = -500 if amount == "A little weight" else -700

    # Total daily calories
    total_calories = base_calories[weight] + calorie_adjustment

    # Meal distribution
    meals = {
        "Breakfast": total_calories * 0.3,
        "Lunch": total_calories * 0.3,
        "Dinner": total_calories * 0.4
    }

    return meals[meal_time]

def get_meal_recommendation(user_name,goal_choice, amount_choice, pounds_choice, weight_choice, meal_time_choice):
    meal_views = {
        "Breakfast":"v_Breakfast",
        "Lunch":"v_Lunch",
        "Dinner":"v_Dinner"
    }

    meal_view_choice = meal_views[meal_time_choice]
    calories_choice = get_calories(goal_choice, amount_choice, pounds_choice, weight_choice, meal_time_choice)

    cursor = pyodbc.connect(conn_str)

    query = f"""
    SELECT *
    FROM {meal_view_choice}
    WHERE CALORIES = {calories_choice}
    """
    results_df = pd.read_sql_query(query, cursor)

    # Check if the DataFrame has any rows
    if not results_df.empty:
        # Randomly select one row as the recommendation
        recommendation = results_df.iloc[random.randint(0, len(results_df) - 1)]
    else:
        # Set recommendation to None if no rows are returned
        recommendation = None
    delta = 0
    while recommendation is None:
        delta += 10
        cursor = pyodbc.connect(conn_str)

        query = f"""
            SELECT *
            FROM {meal_view_choice}
            WHERE CALORIES >= {calories_choice-delta}
            AND CALORIES <= {calories_choice+delta}
            """
        results_df = pd.read_sql_query(query, cursor)

        # Check if the DataFrame has any rows
        if not results_df.empty:
            # Randomly select one row as the recommendation
            recommendation = results_df.iloc[random.randint(0, len(results_df) - 1)]
        else:
            print("Please Wait...")
            recommendation = None

    if (recommendation is not None):
        upsert_questionnaire_results(user_name,meal_time_choice,calories_choice,"Calories",conn_str)
        return get_recommendation_object(recommendation)
    
    else:
        return {
            "recommendation": "None"
        }

    
def get_muscle_gain_meal(username,current_weight, muscle_gain_goal):
    # Expects both the meal recommendation and a message
    [recommendation, message] = get_protein_recommendation(username,current_weight, muscle_gain_goal)
    if (recommendation is not None):
        return {
            "meal": get_recommendation_object(recommendation),
            "message": message
        }
    
    else:
        return {
            "recommendation": "None"
        }

import pyodbc

