import numpy as np
import pandas as pd
import logging
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_dataset():
    data = pd.DataFrame({
        'feature1': np.random.rand(1000),
        'feature2': np.random.rand(1000),
        'feature3': np.random.rand(1000),
        'feature4': np.random.rand(1000),
        'label': np.random.choice([0, 1], size=1000)
    })
    return data.drop('label', axis=1), data['label']

def train_model(X_train, y_train):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')

    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
    }
    
    grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, scoring='accuracy', cv=3)
    grid_search.fit(X_train_scaled, y_train)

    logging.info(f"Best parameters: {grid_search.best_params_}")

    return grid_search.best_estimator_, scaler

def evaluate_model(model, X_test, y_test):
    X_test_scaled = scaler.transform(X_test)
    
    y_pred = model.predict(X_test_scaled)
    
    logging.info("Model Evaluation:")
    logging.info(classification_report(y_test, y_pred))
    logging.info(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

def detect_threats(model, scaler, incoming_data):
    incoming_data_scaled = scaler.transform(incoming_data)
    
    y_pred = model.predict(incoming_data_scaled)
    
    return "Potential threat detected!" if y_pred[0] == 1 else "Normal traffic"

if __name__ == "__main__":
    X, y = load_dataset()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model, scaler = train_model(X_train, y_train)

    evaluate_model(model, X_test, y_test)

    sample_data = np.array([[0.5, 0.2, 0.6, 0.8]])
    result = detect_threats(model, scaler, sample_data)
    logging.info(result)