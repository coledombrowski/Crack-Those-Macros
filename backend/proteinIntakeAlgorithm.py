import random
import pyodbc
import pandas as pd
import sys
import os
from addMeal import upsert_questionnaire_results

server = 'crackthosemacros.database.windows.net'
database = 'crackthosemacros'
username = 'viewonly'
password = 'CrackThoseMacros!2024'
driver = '{SQL Server}'  # Adjust driver as needed
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_protein_meal_suggestion(username,protein_goal):
    delta = 0
    cursor = pyodbc.connect(conn_str)

    query = f"""
        SELECT *
        FROM v_All_Food_Standardized
        WHERE PROTEIN = {protein_goal}
        AND CALORIES = (SELECT MIN(CALORIES) FROM v_All_Food_Standardized WHERE PROTEIN = {protein_goal})
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
            FROM v_All_Food_Standardized
            WHERE PROTEIN >= {protein_goal-1}
            AND PROTEIN <= {protein_goal+1}
            AND CALORIES = (SELECT MIN(CALORIES) FROM v_All_Food_Standardized WHERE PROTEIN >= {protein_goal-1} AND PROTEIN <= {protein_goal+1})
            """
        results_df = pd.read_sql_query(query, cursor)

        # Check if the DataFrame has any rows
        if not results_df.empty:
            # Randomly select one row as the recommendation
            recommendation = results_df.iloc[random.randint(0, len(results_df) - 1)]
        else:
            print("Please Wait...")
            recommendation = None
    upsert_questionnaire_results(username,"Protein Meal",recommendation['PROTEIN'],"Protein",conn_str)
    return recommendation

def get_protein_recommendation(username,current_weight, muscle_gain_goal):
    if current_weight < 0 or muscle_gain_goal not in [5, 10]:
        return "Invalid input."

    # Calculate protein per meal, user input
    protein_per_meal = 0
    if 0 <= current_weight <= 99:
        if muscle_gain_goal == 5:
            protein_per_meal = 20
        else:
            protein_per_meal = 25
    elif 100 <= current_weight <= 150:
        if muscle_gain_goal == 5:
            protein_per_meal = 30
        else:
            protein_per_meal = 35
    elif 151 <= current_weight <= 200:
        if muscle_gain_goal == 5:
            protein_per_meal = 40
        else:
            protein_per_meal = 45
    elif 201 <= current_weight <= 250:
        if muscle_gain_goal == 5:
            protein_per_meal = 50
        else:
            protein_per_meal = 55
    elif 251 <= current_weight <= 300:
        if muscle_gain_goal == 5:
            protein_per_meal = 60
        else:
            protein_per_meal = 65
    else:
        return "Weight out of range."
    
    meal_rec = get_protein_meal_suggestion(username,protein_per_meal)
    message = (f"{current_weight} lb looking to gain {muscle_gain_goal} pounds of muscle\n"
               f"Display message: “To meet your muscle gain goal, you need to consume "
               f"an average of {protein_per_meal} grams of protein per meal”"
               f"\n"
               f"Meal suggestion:\n"
               f"{meal_rec}"
               )
    print(message)
    return meal_rec, message

# def main():
#     # CTM user inputs
#     muscle_gain_goal = int(input("How much muscle would you like to gain? (5 or 10 pounds) → "))
#     current_weight = int(input("Current weight: "))

#     recommendation = get_protein_recommendation(current_weight, muscle_gain_goal)

# if __name__ == "__main__":
#     main()
