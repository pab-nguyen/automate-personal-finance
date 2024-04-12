import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score


# Load data from Excel
data = pd.read_excel("./data/other_input/Master Ledger.xlsx", sheet_name="Master Ledger")
data = data[data['Date'].dt.year.isin([2022,2023])]

# Extract features and targets
features = ['Account', 'Item', 'Transaction Type', 'Account Type', 'Real Amount', 'Date']
target_columns = ['Categories', 'Categories 2']

X = data[features]
y = data[target_columns]

# Combine "Categories" and "Categories 2" into a single target column
y_combined = y['Categories'] + ':' + y['Categories 2']

# Convert "Date" column to datetime format
X_copy = X.copy()
X_copy['Date'] = pd.to_datetime(X_copy['Date'])

# Extract relevant features from the "Date" column
X_copy['Year'] = X_copy['Date'].dt.year
X_copy['Month'] = X_copy['Date'].dt.month
X_copy['Day'] = X_copy['Date'].dt.day
X_copy['Weekday'] = X_copy['Date'].dt.weekday

# Drop the original "Date" column
X_copy.drop(columns=['Date'], inplace=True)

# Preprocess categorical columns with one-hot encoding
categorical_columns = ['Account', 'Item', 'Transaction Type', 'Account Type']
X_encoded = pd.get_dummies(X_copy, columns=categorical_columns, drop_first=True)

# Split data into training and testing sets
X_train, X_test, y_train_combined, y_test_combined = train_test_split(X_encoded, y_combined, test_size=0.2)

# Encode target variable into integer labels
label_encoder_combined = LabelEncoder()
y_train_combined_encoded = label_encoder_combined.fit_transform(y_train_combined)

# Initialize StandardScaler
scaler = StandardScaler()

# Fit and transform the scaled features on your training data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize models
models = {
    "Random Forest": RandomForestClassifier(),
    # "XGBoost": XGBClassifier(),
    # "SVM": SVC(),
    # "Gradient Boosting": GradientBoostingClassifier(subsample=0.8),
    # "MLP": MLPClassifier(),
    # "KNN": KNeighborsClassifier(),
    # "Logistic Regression": LogisticRegression(),
    # "Naive Bayes": GaussianNB(),
    # "Decision Tree": DecisionTreeClassifier(),
    # "AdaBoost": AdaBoostClassifier(),
    # "Extra Trees": ExtraTreesClassifier(),
    # "CatBoost": CatBoostClassifier(verbose=False)  # Set verbose to False to avoid excessive output
}

# Train and evaluate each model
for model_name, model in models.items():
    print(f"Training and evaluating {model_name}...")
    model.fit(X_train_scaled, y_train_combined_encoded)  # Use scaled data
    predictions_combined = model.predict(X_test_scaled)
    
    # Decode the combined labels to separate "Categories" and "Categories 2"
    predictions_combined_labels = label_encoder_combined.inverse_transform(predictions_combined)
    predictions_categories, predictions_categories2 = zip(*[label.split(':') for label in predictions_combined_labels])
    
    # Calculate accuracy for each category separately
    accuracy_cat = accuracy_score(y_test_combined.str.split(':').str[0], predictions_categories)
    accuracy_cat2 = accuracy_score(y_test_combined.str.split(':').str[1], predictions_categories2)
    
    print(f"{model_name} Accuracy for Categories:", accuracy_cat)
    print(f"{model_name} Accuracy for Categories 2:", accuracy_cat2)
    print("\n")

    # Create a DataFrame to store wrong predictions and corresponding features
    wrong_predictions_df = pd.DataFrame(columns=['Item', 'Account', 'Real Amount', 'Transaction Type', 'Account Type', 'Predicted Categories', 'Predicted Categories 2', 'Actual Categories', 'Actual Categories 2'])

    # Loop through each test data instance and its corresponding prediction
    for i, (prediction, actual, features) in enumerate(zip(predictions_combined_labels, y_test_combined, X_test.iterrows())):
        predicted_cat, predicted_cat2 = prediction.split(':')
        actual_cat, actual_cat2 = actual.split(':')
        _, features = features
        
         # Check if the prediction was wrong
        if (predicted_cat != actual_cat) or (predicted_cat2 != actual_cat2):
            item_description = None
            account = None
            transaction_type = None
            account_type = None

            # Iterate through columns to find the account column
            for column_name, value in features.items():
                if column_name.startswith('Account_') and value:
                    account = column_name.replace('Account_', '')  # Extract the item description

                if column_name.startswith('Item_') and value:
                    item_description = column_name.replace('Item_', '')  # Extract the item description
                    
                if column_name.startswith('Transaction Type_') and value:
                    transaction_type = column_name.replace('Transaction Type_', '')  # Extract the item description
                    
                if column_name.startswith('Account Type_') and value:
                    account_type = column_name.replace('Account Type_', '')  # Extract the item description
                    
            real_amount = features['Real Amount']
            
            # Append the data to the DataFrame
            wrong_predictions_df.loc[i] = [item_description, account, real_amount, transaction_type, account_type, predicted_cat, predicted_cat2, actual_cat, actual_cat2]


    # Save the wrong predictions to a CSV file
    results_filename = f'results_{model_name}.csv'
    wrong_predictions_df.to_csv(results_filename, index=False)

    
