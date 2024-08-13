import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./css/App.css"
import CreateAccount from "./pages/CreateAccount";
import LoginPage from "./pages/LoginPage";
import Questionnaire from "./pages/Questionnaire";
import GetMealSuggestionPage from "./pages/GetMealSuggestion";
import MealSuggestionResult from './pages/MealSuggestionResult';
import UserDashboard from "./pages/UserDashboard";
import HomePage from "./pages/HomePage";
import Logout from "./pages/Logout";
import Navbar from "./components/Navbar";
import GlobalStyle from "./css/GlobalStyle";


function App() {
	return (
		// Add a Route for the Pages and indicate the desired URL path
		<>
			<GlobalStyle />
			<BrowserRouter>
				<div className="Navbar">
					<Navbar />
				</div>
				<div className="App">
					<div className="pages">
						<Routes>
							{/* A default path to redirect back to Home */}
							<Route
								path="*"
								element={<Navigate to="/" />}
							/>
							<Route
								exact path="/"
								element={<HomePage />}
							/>
							<Route
								path="/createAccount"
								element={<CreateAccount />}
							/>
							<Route
								path="/loginPage"
								element={<LoginPage />}
							/>
							<Route
								path="/questionnaire"
								element={<Questionnaire />}
							/>
							<Route
								path="/getMealSuggestion"
								element={<GetMealSuggestionPage />}
							/>
							<Route path="/meal-suggestion-result" element={<MealSuggestionResult />} />
							<Route
								path="/userDashboard"
								element={<UserDashboard />}
							/>
							<Route
								path="/logout"
								element={<Logout />}
							/>
						</Routes>
					</div>
				</div>
			</BrowserRouter>
		</>
	);
}
export default App;
