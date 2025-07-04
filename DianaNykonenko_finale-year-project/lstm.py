"""
LSTM model
Run to train the model, needs data_preprocessing.py
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pandas.tseries.offsets import BDay
from sklearn.metrics import r2_score, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
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

def calculate_mape(actual, predicted):                                                                     # functions for evauation
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

X_train, y_train = np.array(data_prep.X_train), np.array(data_prep.y_train)

def create_model(trial):                                                                                   # model base 
    units = trial.suggest_int("units", 16, 128, step=16)                                               
    dropout = trial.suggest_float("dropout", 0.0, 0.5)
    learning_rate = trial.suggest_float("lr", 1e-4, 1e-2, log=True)

    model = Sequential()
    model.add(LSTM(units=units, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(dropout))
    model.add(LSTM(units=units, return_sequences=False))
    model.add(Dropout(dropout))
    model.add(Dense(units=10, activation='linear'))

    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mse')

    return model

def objective(trial):                                                                                      # optuna optimiser to find the best hyperparameters
    model = create_model(trial)
    epochs = trial.suggest_int("epochs", 20, 100, step=10)
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])

    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)
    loss = history.history["loss"][-1]
    return loss

optuna.logging.set_verbosity(optuna.logging.INFO)
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=5)                                                                     # adjust for faster performans or better results (each trial - one training of the model)

print("Best hyperparameters:", study.best_params)

best_params = study.best_params
model = create_model(study.best_trial)

model.fit(X_train, y_train, epochs=best_params["epochs"], 
          batch_size=best_params["batch_size"], 
          verbose=1)

num_days = 10                                                                                             # number of days should be changed here too if changed above                                        
today = datetime.today().date()
start_date = today - BDay(7 + num_days)
end_date = start_date + BDay(num_days)

predicted_prices = data_prep.multi_step_forecast_lstm(model, num_days=num_days)
print("\nPredicted Prices:")
for i, price in enumerate(predicted_prices, start=1):
    print(f"Day {i} ({start_date + BDay(i-1)}): ${price:.2f}")

actual_prices = data_prep.fetch_actual_prices(start_date, end_date)
min_length = min(len(actual_prices), len(predicted_prices))

r2 = r2_score(actual_prices[:min_length], predicted_prices[:min_length])                                   # evaluation, calls the defined functions
mape = calculate_mape(actual_prices[:min_length], predicted_prices[:min_length])
rmse = calculate_rmse(actual_prices[:min_length], predicted_prices[:min_length])

print(f"R² Score: {r2:.4f}")
print(f"MAPE: {mape:.4f}%")
print(f"RMSE: {rmse:.4f}")

plus_di, minus_di = calculate_dmi(data_prep.df)
plus_di_recent = plus_di[-min_length:]
minus_di_recent = minus_di[-min_length:]
dmi_acc = dmi_directional_accuracy(predicted_prices[:min_length], plus_di_recent, minus_di_recent)

print(f"DMI Directional Accuracy: {dmi_acc:.2f}%")
plot_predictions(predicted_prices, actual_prices, start_date)