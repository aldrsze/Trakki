# Trakki - Personal Finance Tracker

Trakki is a Python-based desktop application built with Tkinter that helps you effortlessly track your income, expenses, and savings goals. It also features a built-in AI Financial Coach powered by the Groq API to provide personalized financial insights and advice.

## Features
* **Dashboard & Analytics:** View your current balance, total income, expenses, and savings at a glance with visual charts.
* **Expense & Income Tracking:** Add, edit, and remove transactions to keep your finances up to date.
* **Savings Goals:** Set target savings goals, track your progress, and manage funds dedicated to specific items.
* **AI Financial Coach:** Chat with a built-in AI assistant that analyzes your current financial data and provides actionable, personalized advice in English and Tagalog.
* **Transaction History:** Review all your past financial activities in a clean table view.

## Prerequisites
* Python 3.x

## Installation & Setup

1. **Download the Project**
   Extract the project files into a single folder on your computer.

2. **Install Dependencies**
      Open your terminal/command prompt, navigate to the project folder, and run:
         ```bash
            pip install -r requirements.txt
               ```

 3. **Set Up the AI Coach (Environment Variables)**
    * Create a new file named exactly `.env` in the main project folder.
    * Get a free API key from the [Groq Console](https://console.groq.com).
    * Add your key to the `.env` file like this:
    ```text
    GROQ_API_KEY=your_api_key_here
    ```

4. **Run the Application**
    ```bash
    python main.py
    ```

## Tech Stack
* **GUI Framework:** Tkinter
* **Data Visualization:** Matplotlib
* **AI Integration:** Groq API (via the `requests` library)

##  
-Aldrsze.
