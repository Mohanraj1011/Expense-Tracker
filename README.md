# Expense-Tracker
### Personal Expense Tracker and Financial Assistant

**Overview**

The Personal Expense Tracker and Financial Assistant is a comprehensive web application designed to help users manage their expenses effectively while providing tools for financial planning and assistance. It integrates various features to cater to both expense tracking and financial guidance through AI-powered chatbots.

**Features**

1. **Expense Tracking**:
   - **Add Expense**: Users can log their expenses with details such as description, amount, date, and category (groceries, utilities, entertainment, etc.).
   - **View Expenses**: Allows users to see a detailed list of their expenses, including descriptions, amounts, categories, and dates.
   - **Monthly Reports**: Provides visual insights into monthly expenses through charts, helping users analyze spending patterns over time.

2. **Financial Goals**:
   - **Set Goals**: Users can set financial goals specifying the description, target amount, and deadline.
   - **Track Progress**: Monitor the progress towards goals with real-time updates on savings and expenditure.

3. **AI-Powered Financial Assistance**:
   - **Chatbot Integration**: Includes an AI chatbot capable of answering financial queries, providing insights on budgeting, saving tips, and investment strategies.
   - **Expense Prediction**: Predicts future expenses using machine learning models, helping users plan their finances more effectively.

4. **User Authentication and Security**:
   - **User Registration and Login**: Secure user registration and login functionality using encrypted passwords.
   - **Data Privacy**: Ensures user data privacy with secure storage and access controls.

**Technology Stack**

- **Backend**: Python with Flask framework for handling HTTP requests, integrating machine learning models for expense prediction.
- **Database**: SQLite database managed using SQLAlchemy for storing user information, expenses, and financial goals.
- **Frontend**: HTML, CSS, and JavaScript for user interface design, integrating with Bootstrap for responsive layouts.
- **Machine Learning**: Utilizes scikit-learn for training and deploying machine learning models, such as linear regression for expense prediction.
- **AI Chatbot**: Integrates with Dialogflow for natural language processing (NLP) and understanding user queries related to personal finance.

**Dataset**

- Utilizes a SQLite database (`expense_tracker.db`) to store user-related information, expenses, financial goals, and income data.

**Deployment**

- Deployed locally for development purposes with plans for future deployment on cloud platforms like AWS or Heroku for scalability.

**Conclusion**

The Personal Expense Tracker and Financial Assistant aims to empower users with tools to manage their finances efficiently, track expenses, set financial goals, and receive personalized financial advice through AI chatbots. It combines usability with advanced technologies to enhance financial management and planning capabilities.

**Future Enhancements**

- Integration with external financial APIs for real-time financial data.
- Enhanced machine learning models for more accurate expense predictions.
- Mobile application development for broader accessibility and convenience.

This project not only facilitates expense management but also educates users about financial planning and budgeting, promoting better financial habits and decision-making.
