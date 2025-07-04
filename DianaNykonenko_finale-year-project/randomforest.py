"""
Random Forest model
Run to train the model, needs data_preprocessing.py
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error
from pandas.tseries.offsets import BDay
from data_preprocessing import DataPreProcessing
import talib as tb
import optuna

def plot_predictions(predicted_prices, actual_prices, start_date):
    dates = [start_date + timedelta(days=i) for i in range(len(predicted_prices))]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, predicted_prices, label="Predicted Prices", marker='o', linestyle='dashed')
    plt.plot(dates[:len(actual_prices)], actual_prices, label="Actual Prices", marker='x', linestyle='solid')
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title("Stock Price Prediction vs Actual")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def calculate_mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

def calculate_rmse(actual, predicted):
    return np.sqrt(mean_squared_error(actual, predicted))

def calculate_dmi(df):
    high = df['High'].values.flatten()
    low = df['Low'].values.flatten()
    close = df['Close'].values.flatten()
    plus_di = tb.PLUS_DI(high, low, close, timeperiod=14)
    minus_di = tb.MINUS_DI(high, low, close, timeperiod=14)
    return plus_di, minus_di

def dmi_directional_accuracy(predicted, plus_di, minus_di):
    correct = 0
    total = len(predicted) - 1
    for i in range(total):
        pred_direction = np.sign(predicted[i+1] - predicted[i])
        dmi_direction = 1 if plus_di[i] > minus_di[i] else -1
        if pred_direction == dmi_direction:
            correct += 1
    return (correct / total) * 100

data_prep = DataPreProcessing(seq_length=10, num_days_ahead=10)                                            # number of days for the prediction, can be changed
data_prep.input()
data_prep.fetch()
data_prep.preprocess()
data_prep.heatmap()

X_train, y_train = data_prep.X_train, data_prep.y_train
X_train_2d = X_train.reshape(X_train.shape[0], -1)

def objective(trial):                                                                                      # optuna optimiser to find the best hyperparameters                      
    params = {
    "n_estimators": trial.suggest_int("n_estimators", 40, 80), 
    "max_depth": trial.suggest_int("max_depth", 5, 40),
    "min_samples_split": trial.suggest_int("min_samples_split", 5, 15),
    "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 5) 
}

    model = RandomForestRegressor(**params, random_state=42, n_jobs=-1)                                    # model base 
    model.fit(X_train_2d, y_train)

    predicted_prices = data_prep.multi_step_forecast(model, num_days=10)

    today = datetime.today().date()
    start_date = today - BDay(17)
    end_date = start_date + BDay(10)
    actual_prices = data_prep.fetch_actual_prices(start_date, end_date)

    min_len = min(len(predicted_prices), len(actual_prices))
    return calculate_rmse(np.array(actual_prices[:min_len]), np.array(predicted_prices[:min_len]))

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=10)                                                                     # adjust for faster performans or better results (each trial - one training of the model)

print("Best Parameters:", study.best_params)

best_model = RandomForestRegressor(**study.best_params, random_state=42, n_jobs=-1)
best_model.fit(X_train_2d, y_train)
num_days = 10                                                                                               # number of days should be changed here too if changed above    
today = datetime.today().date()
start_date = today - BDay(7 + num_days)
end_date = start_date + BDay(num_days)

predicted_prices = data_prep.multi_step_forecast(best_model, num_days=num_days)
actual_prices = data_prep.fetch_actual_prices(start_date, end_date)

min_length = min(len(actual_prices), len(predicted_prices))              
r2 = r2_score(actual_prices[:min_length], predicted_prices[:min_length])                                    # evaluation, calls the defined functions
mape = calculate_mape(actual_prices[:min_length], predicted_prices[:min_length])
rmse = calculate_rmse(actual_prices[:min_length], predicted_prices[:min_length])

plus_di, minus_di = calculate_dmi(data_prep.df)
plus_di_recent = plus_di[-min_length:]
minus_di_recent = minus_di[-min_length:]
dmi_acc = dmi_directional_accuracy(predicted_prices[:min_length], plus_di_recent, minus_di_recent)

print(f"\nFinal Evaluation:")
print(f"R² Score: {r2:.4f}")
print(f"MAPE: {mape:.2f}%")
print(f"RMSE: {rmse:.2f}")
print(f"DMI Directional Accuracy: {dmi_acc:.2f}%")

plot_predictions(predicted_prices, actual_prices, start_date)