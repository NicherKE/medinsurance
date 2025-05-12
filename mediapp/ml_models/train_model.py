import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error
import xgboost as xgb
import joblib
import warnings

# Configuration
PLOT_PATH = './sampleImages/'
MODEL_PATH = 'mediapp/ml_models/insurance_model.pkl'

# Set modern pandas options
pd.set_option('future.no_silent_downcasting', True)
warnings.filterwarnings('ignore', category=FutureWarning)

def load_and_preprocess_data():
    #Load and properly preprocess the insurance data
    data = pd.read_csv('./mediapp/ml_models/insurance.csv')
    
    # Modern categorical conversion
    cat_mapping = {
        'sex': {'male': 0, 'female': 1},
        'smoker': {'no': 0, 'yes': 1},
        'region': {'northwest': 0, 'northeast': 1, 'southeast': 2, 'southwest': 3}
    }
    data = data.replace(cat_mapping).infer_objects(copy=False)
    
    return data

def perform_eda(data):
    #Modernized EDA with updated seaborn functions"""
    # Correlation plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.corr(), cmap='BuPu', annot=True, fmt=".2f")
    plt.title("Medical Charges Correlations")
    plt.tight_layout()
    plt.savefig(f'{PLOT_PATH}correlation.png')
    plt.close()
    
    # Distribution plots
    for col in ['age', 'bmi', 'charges']:
        plt.figure(figsize=(10, 7))
        sns.histplot(data[col], kde=True, bins=30)
        plt.title(f'Distribution of {col}')
        plt.savefig(f'{PLOT_PATH}{col}_distribution.png')
        plt.close()

def prepare_model_data(data):
    #Prepare scaled data for modeling"""
    X = data.drop('charges', axis=1)
    y = data['charges']
    
    # Scale only numerical features
    scaler = StandardScaler()
    for col in ['age', 'bmi']:
        X[col] = scaler.fit_transform(X[[col]])
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    #Train and evaluate all models"""
    models = {
        'LinearRegression': LinearRegression(),
        'Ridge': Ridge(alpha=20, random_state=42),
        'SVR': SVR(C=10, gamma=0.1, tol=0.0001),
        'RandomForest': RandomForestRegressor(
            max_depth=50, min_samples_leaf=12,
            min_samples_split=7, n_estimators=1200
        ),
        'XGBoost': xgb.XGBRegressor(objective='reg:squarederror')
    }
    
    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        cv_score = cross_val_score(model, X_train, y_train, cv=10).mean()
        
        metrics = {
            'Model': name,
            'RMSE': np.sqrt(mean_squared_error(y_test, model.predict(X_test))),
            'R2_Score(train)': r2_score(y_train, model.predict(X_train)),
            'R2_Score(test)': r2_score(y_test, model.predict(X_test)),
            'Cross-Validation': cv_score
        }
        results.append(metrics)
    
    return pd.DataFrame(results)

def visualize_results(results_df):
    #Modern visualization with proper hue handling
    plt.figure(figsize=(12, 7))
    ax = sns.barplot(
        x='Cross-Validation',
        y='Model',
        hue='Model',
        data=results_df.sort_values('Cross-Validation'),
        palette='Reds',
        legend=False
    )
    
    # Add value labels
    for i, val in enumerate(results_df.sort_values('Cross-Validation')['Cross-Validation']):
        ax.text(val + 0.01, i, f'{val:.3f}', va='center')
    
    plt.title('Model Performance Comparison', pad=20)
    plt.xlabel('Cross-Validation Score')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(f'{PLOT_PATH}model_comparison.png', dpi=300)
    plt.close()

def save_best_model(models, X_train):
    #Save the best performing model
    # Select LinearRegression as specified 
    best_model = models['LinearRegression']
    joblib.dump(best_model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

def main():
    # Data pipeline
    data = load_and_preprocess_data()
    perform_eda(data)
    X_train, X_test, y_train, y_test = prepare_model_data(data)
    
    # Model pipeline
    results_df = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    visualize_results(results_df)
    save_best_model({
        'LinearRegression': LinearRegression().fit(X_train, y_train),
        'RandomForest': RandomForestRegressor().fit(X_train, y_train)
    }, X_train)
    
    print(results_df.sort_values('Cross-Validation', ascending=False))

# Ensure DataFrame column names are preserved
X = data[['age', 'sex', 'bmi', 'children', 'smoker', 'region']]  # Use DataFrame, not values
y = data['charges']

# This will preserve feature names in the model
model.fit(X, y)


if __name__ == '__main__':
    main()