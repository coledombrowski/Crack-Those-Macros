import random
import pyodbc
import pandas as pd
from backend.addMeal import accept_meal_entry

server = 'crackthosemacros.database.windows.net'
database = 'crackthosemacros'
username = 'viewonly'
password = 'CrackThoseMacros!2024'
driver = '{SQL Server}'  # Adjust driver as needed
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_choice(options):
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    choice = int(input("Enter the number of your choice: ")) - 1
    return choice

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


def get_meal_recommendation():
    goals = ["Gain weight", "Maintain weight", "Lose weight"]
    amounts = ["More weight", "A little weight"]
    pounds_options = {"Gain weight": [15, 20], "Lose weight": [5, 10]}
    meal_times = ["Breakfast", "Lunch", "Dinner"]
    meal_views = {
        "Breakfast":"v_Breakfast",
        "Lunch":"v_Lunch",
        "Dinner":"v_Dinner"
    }
    weights = ["0-99 lb", "100-150 lb", "151-200 lb", "201-250 lb", "251-300 lb"]

    print("Select your health goal:")
    goal_choice = get_choice(goals)

    #initialization of variables to reduce errors
    amount_choice = "More weight"
    pounds_choice = 0
    delta = 0

    if goal_choice == 0:  # Gain weight
        print("Select the amount of weight you want to gain:")
        amount_choice = amounts[get_choice(amounts)]

        print("Select the specific pounds:")
        pounds_choice = pounds_options["Gain weight"][get_choice(pounds_options["Gain weight"])]

        print("Select the meal time:")
        meal_time_choice = meal_times[get_choice(meal_times)]
        meal_view_choice = meal_views[meal_time_choice]

        print("Select your weight range:")
        weight_choice = weights[get_choice(weights)]

    elif goal_choice == 1:  # Maintain weight choice
        print("Select the meal time:")
        meal_time_choice = meal_times[get_choice(meal_times)]
        meal_view_choice = meal_views[meal_time_choice]

        print("Select your weight range:")
        weight_choice = weights[get_choice(weights)]

    elif goal_choice == 2:  # Lose weight choice
        print("Select the amount of weight you want to lose:")
        amount_choice = amounts[get_choice(amounts)]

        print("Select the specific pounds:")
        pounds_choice = pounds_options["Lose weight"][get_choice(pounds_options["Lose weight"])]

        print("Select the meal time:")
        meal_time_choice = meal_times[get_choice(meal_times)]
        meal_view_choice = meal_views[meal_time_choice]

        print("Select your weight range:")
        weight_choice = weights[get_choice(weights)]

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
    print(recommendation)
    accept_meal_entry(recommendation)
    return recommendation

get_meal_recommendation()