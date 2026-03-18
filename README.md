# Inventory Forecasting MVP

This project is a cyber-physical forecasting system designed to predict inventory levels based on historical data. The MVP is built to demonstrate that the system can accurately forecast when inventory will fall below critical levels and notify managers accordingly. 

The project is divided among five roles:
- **Team Member A: Data Engineer**
- **Team Member B: Model Engineer**
- **Team Member C: Backend Developer**
- **Team Member D: Frontend Developer**
- **Team Member E: Notifications Developer**

This README explains what has been completed so far (Data & Model Engineering) and details the tasks and integration points for the remaining team members.

---

## Table of Contents

- [Overview](#overview)
- [Completed Work (Data & Model Engineering)](#completed-work-data--model-engineering)
- [Tasks for Remaining Team Members](#tasks-for-remaining-team-members)
  - [Team Member C: Backend Developer](#team-member-c-backend-developer)
  - [Team Member D: Frontend Developer](#team-member-d-frontend-developer)
  - [Team Member E: Notifications Developer](#team-member-e-notifications-developer)
- [Integration Process & Quality Control](#integration-process--quality-control)
- [How to Run](#how-to-run)
- [Future Improvements](#future-improvements)
- [Contact](#contact)

---

## Overview

The Inventory Forecasting MVP is intended to:
- **Collect and clean data** on sales, current stock, and delivery dates.
- **Train a machine learning model** (currently Linear Regression) to forecast future inventory levels.
- **Expose the prediction functionality via a Flask API** so that non-technical users can interact with the system through a web dashboard.
- **Notify managers** when inventory reaches a critical threshold (to be implemented by the Notifications Developer).
- **Provide a shared baseline** for backend, frontend, and notification integration during MVP development.

### Practical Problem This Now Solves

The backend now targets a real operations problem: **preventing stockouts while avoiding unnecessary over-ordering**.

It provides:
- **Latest inventory snapshot per item** (`GET /inventory/summary`)
- **Reorder planning recommendations** with lead-time and demand logic (`GET /inventory/reorder-plan`)
- **Item-aware forecasting** (`GET /predict?date=YYYY-MM-DD&item=<name>`)

---

## Completed Work (Data & Model Engineering)

### Data Engineering (Team Member A)
- **Data Collection & Preparation:**
  - Collected historical data on sales, stock levels, and delivery dates.
  - Created a standardized CSV file (`data/cleaned_data.csv`) ensuring that column names are consistent (e.g., `date`, `item`, `sold`, `stock`, `delivery_time`).
- **Data Cleaning & Validation:**
  - Removed missing or invalid entries.
  - Verified that values (such as sales numbers and dates) are logical (e.g., no negative sales, dates not in the future).
- **Preliminary Analysis:**
  - Performed initial analysis using pandas functions (`head()`, `describe()`, `info()`) to ensure data quality.

### Model Engineering (Team Member B)
- **Model Selection & Training:**
  - Chose a Linear Regression model for the MVP.
  - Preprocessed data by:
    - Converting date fields into numeric (ordinal) representations.
    - Calculating the difference in days between `date` and `delivery_time`.
    - One-hot encoding the `item` category.
  - Split data into training and testing sets and trained the model.
  - Evaluated model performance using metrics such as Mean Squared Error (MSE) and R² score.
- **Saving Model & Prediction Function:**
  - Saved the trained model as `models/demand_forecast.pkl`.
  - Saved the list of feature columns used during training as `models/feature_columns.pkl`.
  - Developed a prediction function in `src/predict_inventory.py` that loads the model and processes new input data to predict inventory levels.

---

## Tasks for Remaining Team Members

### Team Member C: Backend Developer
**Your tasks are to:**
- **Develop the Flask API:**
  - Create endpoints such as:
    - `GET /predict?day=YYYY-MM-DD` – to return the predicted inventory level for the specified date.
    - `GET /inventory` – to return the current inventory levels (this can either use the CSV file or query a database if one is implemented).
- **Integrate with the ML Model:**
  - Load the trained model (`demand_forecast.pkl`) and feature columns (`feature_columns.pkl`) using the prediction functions provided in `src/predict_inventory.py`.
  - When a prediction request is received, call the `predict_inventory()` function to generate a forecast.
- **Error Handling:**
  - Validate user inputs (e.g., correct date format, valid day values).
  - Return clear JSON error messages (HTTP 400/404) if data is missing or inputs are invalid.
- **Quality Control:**
  - Test endpoints using tools like Postman or curl to ensure that JSON responses are correctly formatted.
  - Ensure that API endpoints are robust and handle exceptions gracefully.

### Team Member D: Frontend Developer
**Your tasks are to:**
- **Design the User Interface:**
  - Create a minimalist HTML/CSS interface that displays:
    - A table showing current inventory levels.
    - A form to enter a date for which the inventory forecast will be generated.
  - Ensure that the interface is user-friendly and visually appealing.
- **Implement JavaScript for API Calls:**
  - On page load, fetch data from the `/inventory` endpoint to display current stock.
  - Add an event listener for a button (e.g., "Predict Inventory") that sends a request to the `/predict?day=YYYY-MM-DD` endpoint.
  - Parse the returned JSON and update the interface with the prediction.
- **Quality Control:**
  - Validate that the page works on common browsers without JavaScript errors.
  - Ensure that data is correctly displayed and the interface updates promptly when a prediction is requested.

### Team Member E: Notifications Developer
**Your tasks are to:**
- **Implement the Notification System:**
  - Create a Telegram bot using BotFather and obtain the `TELEGRAM_BOT_TOKEN`.
  - Develop a function/script that checks current inventory levels by calling the `/inventory` endpoint.
- **Set Up Low Inventory Alerts:**
  - Define a threshold for low inventory.
  - If any product’s stock falls below the threshold, send an informative notification via Telegram. The message should include:
    - The product name.
    - The current inventory level.
    - A link to the web dashboard (if available).
- **Integration Options:**
  - Either implement a dedicated `/alert` endpoint in the Flask API that triggers notifications,
  - Or schedule the notification function to run periodically (e.g., using a scheduler like `schedule` or a cron job).
- **Quality Control:**
  - Test the notification function by simulating low inventory conditions.
  - Ensure that the alert messages are clear, timely, and include all necessary details.

---

## Integration Process & Quality Control

- **Data Flow:**
  - **Data Engineer** provides the cleaned CSV (`data/cleaned_data.csv`).
  - **Model Engineer** uses this file to train and save the model (saved as `models/demand_forecast.pkl` and `models/feature_columns.pkl`).
  - **Backend Developer** loads the model and exposes endpoints that are consumed by the Frontend and Notification systems.
  - **Frontend Developer** builds the user interface that calls these endpoints and displays the predictions.
  - **Notifications Developer** uses the same backend endpoints to monitor stock levels and send alerts.
  
- **Testing:**
  - **Unit Tests:** Each team should create tests for their modules (e.g., testing the `predict_inventory()` function, validating API responses).
  - **Integration Tests:** Run the full pipeline (from data input through model prediction, API response, and front-end display) to ensure all components work together seamlessly.
  - **Regression Tests:** When changes are made (e.g., data format changes), the entire system should be re-tested to ensure no integration points are broken.

---

## How to Run

1. **Clone the Repository and Set Up the Environment:**
   ```bash
   DO CTRL + SHIFT P in the VS CODE, and select git clone then paste <repository link>
   git clone <repository_url>
   cd MVP
   python -m venv venv
   
   # Activate the virtual environment:
   # On Windows: venv\Scripts\activate
   # On macOS/Linux: source venv/bin/activate
   pip install -r requirements.txt


   Here’s a quick and simple way to commit and push your changes to GitHub:  

1. Add changes: Stage the files you changed:  
   ```
   git add .
   ```
   This stages all modified files. You can also specify a file like `git add filename`.

2. Commit changes: Add a message describing what you changed:  
   ```
   git commit -m "Your message here"
   ```
   Keep the message short and descriptive.

3. Push changes: Send your commits to GitHub:  
   ```
   git push origin main
   ```
   Replace `main` with your branch name if it’s different.  

