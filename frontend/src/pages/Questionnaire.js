import React, { useState } from 'react';
import axiosInstance from 'axios';
import { useNavigate } from 'react-router-dom';

const Questionnaire = () => {
	const [step, setStep] = useState(0);
	const [goal, setGoal] = useState('');
	const navigate = useNavigate();
	// User variables for answers
	const [responses, setResponses] = useState({
		goal: '',
		goalWeightChange: '',
		question2: '',
		question3: '',
		question4Ft: '',
		question4In: '',
		question5: '',
		question6: '0',
	});
	// Setting values once the user selects or types in a value
	const handleGoalChange = (event) => {
		setGoal(event.target.value);
	};
	// Moves Step across switch case
	const handleNext = () => {
		if (step === 0 && !goal) {
			alert('Please select a goal');
			console.log("inside Next");
			
		} else {
			setStep(step + 1);
			console.log("step numer is: "+ step)
		}
		if (step === 1 && goal === 'maintain-weight') {
			// setResponses({
			// 	...responses,
			// 	goalWeightChange: '0',
			// 	question6: '0',
			// });
			setStep(2); // Skip step 2
			return;
		}

		if (step === 6) {
			handleSubmit();
		}
	};
	const handleBack = () => {
		if (step === 0){
			//setStep(step);
			console.log("inside back when === 0 ");
		}
		else if (goal === "maintain-weight" && step === 2){
			setStep(0);
			
			console.log("going back with maintain")
		}
		else{
			setStep(step - 1);
			console.log("going back");
		}

	};
	// Saves final answers
	const handleSubmit = async () => {
		const data = {
			goal,
			goalWeightChange: responses.goalWeightChange,
			gender: responses.question2,
			age: responses.question3,
			height_ft: responses.question4Ft,
			height_in: responses.question4In,
			weight_lb: responses.question5,
			muscle_gain: responses.question6,
		};
		// Saving it to backend to server.py
		try {
			const response = await axiosInstance.post('/questionnaire', data);
			if (response.status === 200) {
				const result = response.data;
				console.log('Data saved successfully:', result);
			} else {
				console.error('Error saving data');
			}
		} catch (error) {
			console.error('Error:', error);
		}
	};
	// Handles the answers from user 
	const handleResponseChange = (event) => {
		const { name, value } = event.target;
		setResponses({ ...responses, [name]: value });
	};
	// Checks to see if an answer is blank. If it is, the user can't move forward
	const validateStep = () => {
		switch (step) {
			case 0:
				return goal !== '';
			case 1:
				return responses.goalWeightChange !== '';
			case 2:
				return responses.question6 !== '';
			case 3:
				return responses.question2 !== '';
			case 4:
				return responses.question3 !== '';
			case 5:
				return responses.question4Ft !== '' && responses.question4In !== '';
			case 6:
				return responses.question5 !== '';
			
			default:
				return true;
		}
	};
	// Moves along loading different questions. Could be new pages but for right now it remains on one page
	const renderStep = () => {
		switch (step) {
			case 0:
				return (
					<div>
						<h2>Question 1: Select one that fits your goal</h2>
						<form>
							<div>
								<label>
									<input
										type="radio"
										value="lose-weight"
										checked={goal === 'lose-weight'}
										onChange={handleGoalChange}
									/>
									Lose Weight
								</label>
							</div>
							<div>
								<label>
									<input
										type="radio"
										value="maintain-weight"
										checked={goal === 'maintain-weight'}
										onChange={handleGoalChange}
									/>
									Maintain Weight
								</label>
							</div>
							<div>
								<label>
									<input
										type="radio"
										value="gain-weight"
										checked={goal === 'gain-weight'}
										onChange={handleGoalChange}
									/>
									Gain Weight
								</label>
							</div>
							{/* <div>
								<label>
									<input
										type="radio"
										value="gain-muscle"
										checked={goal === 'gain-muscle'}
										onChange={handleGoalChange}
									/>
									Gain Muscle
								</label>
							</div> */}
						</form>
					</div>
				);
			case 1:
				
				//if (goal === "gain-weight"){
					
			
					
				//}
				 if (goal === "lose-weight"){
					
					return (
					<div>
						<h2>How much weight do you want to lose?</h2>
						<form>
							<div>
								<label>
									<input
										type="number"
										name="goalWeightChange"
										value={responses.goalWeightChange}
										onChange={handleResponseChange}
										min="1"
									/>
								</label>
							</div>
						</form>
					</div>
					);
					
				}
				else if (goal === "gain-weight"){

					return (
					<div>
						<h2>How much weight do you want to gain?</h2>
						<form>
							<div>
								<label>
									<input
										type="number"
										name="goalWeightChange"
										value={responses.goalWeightChange}
										onChange={handleResponseChange}
										min="1"
									/> lb
								</label> 
							</div>
						</form>
					</div>
					);
					
				}
	
				else if (goal === "maintain-weight"){
					responses.goalWeightChange = '0';
					//responses.question6 = '0';
					console.log("Before next step" + step);
					handleNext();
					console.log("After next step" + step);
					
				}
				case 2:
					
				return (
					<div>
						<h2>Question 2: Do you want to gain muscle?</h2>
						<h2>If yes, how much?</h2>
						<form>
							<div>
								<label>
									<input
										type="number"
										name="question6"
										value={responses.question6}
										onChange={handleResponseChange}
										min="0"
									/>lb
									
								</label>
								
							</div>
						</form>
					</div>
					
					);
					
			case 3:
				return (
					<div>
						<h2>Question 3: Male or Female</h2>
						<form>
							<div>
								<label>
									<input
										type="radio"
										name="question2"
										value="male"
										checked={responses.question2 === 'male'}
										onChange={handleResponseChange}
									/>
									Male
								</label>
							</div>
							<div>
								<label>
									<input
										type="radio"
										name="question2"
										value="female"
										checked={responses.question2 === 'female'}
										onChange={handleResponseChange}
									/>
									Female
								</label>
							</div>
						</form>
					</div>
				);
			case 4:
				return (
					<div>
						<h2>Question 4: What is your age?</h2>
						<form>
							<div>
								<label>
									<input
										type="number"
										name="question3"
										value={responses.question3}
										onChange={handleResponseChange}
										min="0"
									/>
								</label>
							</div>
						</form>
					</div>
				);
			case 5:
				return (
					<div>
						<h2>Question 5: What is your height?</h2>
						<form>
							<div>
								<label>
									<input
										type="number"
										name="question4Ft"
										value={responses.question4Ft}
										onChange={handleResponseChange}
										min="0"
									/>
									ft.
								</label>
							</div>
							<label>
								<input
									type="number"
									name="question4In"
									value={responses.question4In}
									onChange={handleResponseChange}
									min="0"
								/>
								in.
							</label>
						</form>
					</div>
				);
			case 6:
				return (
					<div>
						<h2>Question 6: What is your current weight?</h2>
						<form>
							<div>
								<label>
									<input
										type="number"
										name="question5"
										value={responses.question5}
										onChange={handleResponseChange}
										min="0"
									/>
									lb
								</label>
							</div>
						</form>
					</div>
				)
	
			default:
				// Displaying results after questionnaire is complete
				return (
					<div>
						<h2>Summary</h2>
						<p>Goal: {goal} </p>
						<p>Weight Change {responses.goalWeightChange} lb</p>
						<p>Muscle Gain: {responses.question6} lb</p>
						<p>Male or Female: {responses.question2}</p>
						<p>Age: {responses.question3}</p>
						<p>Height: {responses.question4Ft}ft {responses.question4In}in</p>
						<p>Weight: {responses.question5} lb</p>
						<button onClick={() => navigate('/')}>Home</button>
						
					</div>
				);
		}
	};
	//Checks for make sure the form isn't at the last question
	return (
		<div>
			{renderStep()}
			<div>
		
			{step < 7 && (
				<button type="button" onClick={handleNext} disabled={!validateStep()}>
					Next
				</button>
			)}
				{
					step >0 && step < 7 &&(
						<button type = "button" onClick={handleBack}> Back
						</button>
					)}
			</div>
		</div>
	);
};

export default Questionnaire;
