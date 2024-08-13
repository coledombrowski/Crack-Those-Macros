import { createGlobalStyle } from 'styled-components';

// theme colors
const primaryColor = '#FF8C00'; // orange
const secondaryColor = '#FFFFFF'; // white
const backgroundColor = '#F5F5F5'; // light gray for contrast
const textColor = '#333333'; // dark gray for readability
const buttonColor = '#FF4500'; // dark orange for buttons
const buttonHoverColor = '#FF6347'; // reddish orange for button hover effect


const GlobalStyle = createGlobalStyle`
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: 'Roboto', sans-serif;
    }

    body {
        background-color: ${backgroundColor};
        color: ${textColor};
        line-height: 1.6;
    }

    h1, h2, h3, h4, h5, h6 {
        color: ${primaryColor};
    }

    a {
        color: ${primaryColor};
        text-decoration: none;
        &:hover {
            text-decoration: underline;
        }
    }

    button {
        background-color: ${buttonColor};
        border: none;
        border-radius: 5px;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        &:hover {
            background-color: ${buttonHoverColor};
        }
    }

    .container {
        max-width: 1200px;
        margin: auto;
        padding: 20px;
    }

    .card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        padding: 20px;
    }

    .form-control {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ced4da;
        border-radius: 5px;
        font-size: 16px;
    }

    .navbar {
        background-color: ${primaryColor};
        padding: 10px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .navbar a {
        color: white;
        margin-left: 10px;
    }

    .footer {
        background-color: ${secondaryColor};
        color: ${textColor};
        padding: 10px;
        text-align: center;
        border-top: 1px solid ${backgroundColor};
    }
`;

export default GlobalStyle;
