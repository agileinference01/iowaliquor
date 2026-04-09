import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  # or any model you prefer
import joblib

# Load your dataset
print("Loading the dataset...")
data = pd.read_csv('C:\\Users\\PHUyJo3\\OneDrive - NESTLE\\Documents\\projects\\data\\iowa\\GoalMain.csv')

# Display the first few rows of the dataset
print(data.head())

# Assuming your dataset has 'date' and 'sales' columns
# Convert 'date' to datetime format if it's not already
data['date'] = pd.to_datetime(data['date'])

# Extract features and target variable
X = data[['date']]  # You might want to extract more features or process the date
y = data['bottles_sold']

# If you want to use numerical features from the date, you can extract them
X['year'] = X['date'].dt.year
X['month'] = X['date'].dt.month
X['day'] = X['date'].dt.day
X = X.drop('date', axis=1)  # Drop the original date column if not needed

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Regressor model
model = RandomForestRegressor()

# Train the model
model.fit(X_train, y_train)

# Save the model to a .pkl file
joblib.dump(model, 'sales_model.pkl')

print("Model saved as 'sales_model.pkl'")