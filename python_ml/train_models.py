"""
TrainModels - ML Forecasting Suite for Solar Daylight Prediction
Evaluates Linear Regression, Ridge, Random Forest, GBDT, XGBoost, and MLP Regressors.
Auto-detects real-world empirical solar datasets (e.g. 2017_2019.csv / 2017.csv)
and enforces strict chronological train/validation/test splitting to eliminate data leakage.
"""

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

from synthetic_data_generator import generate_annual_dataset

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true > 15.0  # filter nighttime near-zero irradiance
    if np.sum(mask) == 0:
        return 0.0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100.0

def load_dataset():
    # Check for real user dataset candidates
    candidates = [
        os.path.join("..", "Data sets", "2017_2019.csv", "2017_2019.csv"),
        os.path.join("Data sets", "2017_2019.csv", "2017_2019.csv"),
        os.path.join("..", "Data sets", "2017.csv", "2017.csv"),
        os.path.join("Data sets", "2017.csv", "2017.csv"),
        "2017_2019.csv",
        "2017.csv"
    ]

    for path in candidates:
        if os.path.exists(path):
            print(f"[DATASET] Found Real-World Measured Dataset: {path}")
            raw = pd.read_csv(path)
            # Standardize column headers
            raw.columns = [c.strip() for c in raw.columns]
            
            # Feature extraction for real measured dataset
            df = pd.DataFrame()
            df["GHI"] = raw["GHI"]
            df["DNI"] = raw["DNI"]
            df["DHI"] = raw["DHI"]
            df["Temperature"] = raw["Temperature"]
            df["Relative_Humidity"] = raw["Relative Humidity"]
            df["Solar_Zenith_Angle"] = raw["Solar Zenith Angle"]
            df["Wind_Speed"] = raw["Wind Speed"]
            
            # Lag features (T-15m, T-30m, T-60m)
            df["GHI_lag1"] = df["GHI"].shift(1)
            df["GHI_lag2"] = df["GHI"].shift(2)
            df["GHI_lag4"] = df["GHI"].shift(4)
            df["DNI_lag1"] = df["DNI"].shift(1)
            df["zenith_cos"] = np.cos(np.radians(df["Solar_Zenith_Angle"]))

            # Target: 30-minute lookahead GHI (T+2 steps)
            df["target_GHI_30m"] = df["GHI"].shift(-2)
            df = df.dropna()

            feature_cols = ["GHI", "DNI", "DHI", "Temperature", "Relative_Humidity", "GHI_lag1", "GHI_lag2", "GHI_lag4", "DNI_lag1", "zenith_cos"]
            return df[feature_cols].values, df["target_GHI_30m"].values, f"Real-World Measured 3-Year PSM Dataset ({len(df)} samples)"

    # Fallback to synthetic generator
    csv_file = "synthetic_daylight_1year.csv"
    if not os.path.exists(csv_file):
        raw = generate_annual_dataset(csv_file)
    else:
        raw = pd.read_csv(csv_file)
    
    raw["GHI_lag1"] = raw["GHI_W_m2"].shift(1)
    raw["GHI_lag2"] = raw["GHI_W_m2"].shift(2)
    raw["GHI_lag4"] = raw["GHI_W_m2"].shift(4)
    raw["cloud_lag1"] = raw["cloud_factor"].shift(1)
    raw["alt_sin"] = np.sin(np.radians(raw["solar_altitude_deg"]))
    raw["az_cos"] = np.cos(np.radians(raw["solar_azimuth_deg"]))
    raw["target_GHI_30m"] = raw["GHI_W_m2"].shift(-2)
    raw = raw.dropna()

    feature_cols = ["GHI_W_m2", "DNI_W_m2", "DHI_W_m2", "GHI_lag1", "GHI_lag2", "GHI_lag4", "cloud_lag1", "alt_sin", "az_cos"]
    return raw[feature_cols].values, raw["target_GHI_30m"].values, f"Synthetic Dataset ({len(raw)} samples)"

def build_features_and_train():
    X, y, provenance = load_dataset()
    print(f"\n[INFO] Training ML Models on {provenance}...")

    # Chronological Split (70% Train, 15% Validation, 15% Test)
    n = len(X)
    n_train = int(n * 0.70)
    n_val = int(n * 0.15)

    X_train, y_train = X[:n_train], y[:n_train]
    X_val, y_val = X[n_train:n_train+n_val], y[n_train:n_train+n_val]
    X_test, y_test = X[n_train+n_val:], y[n_train+n_val:]

    print(f"Dataset Split -> Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

    models = {
        "Linear Regression (Baseline)": LinearRegression(),
        "Ridge Regression (L2)": Ridge(alpha=1.0),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
        "Gradient Boosting (GBDT)": GradientBoostingRegressor(n_estimators=100, max_depth=6, random_state=42),
        "XGBoost Regressor": xgb.XGBRegressor(n_estimators=120, max_depth=6, learning_rate=0.08, random_state=42),
        "MLP Neural Regressor": MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42)
    }

    results = []

    print("\n" + "="*85)
    print(f"{'MODEL':<30} | {'MAE (W/m²)':<10} | {'RMSE (W/m²)':<11} | {'R² SCORE':<10} | {'MAPE (%)':<8}")
    print("="*85)

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        mape = mean_absolute_percentage_error(y_test, preds)

        results.append({
            "Model": name,
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2": round(r2, 4),
            "MAPE": round(mape, 2)
        })

        print(f"{name:<30} | {mae:<10.2f} | {rmse:<11.2f} | {r2:<10.4f} | {mape:<8.2f}")

    print("="*85)
    print(f"Data Provenance: Evaluated strictly on chronological test set from {provenance}.")
    return results

if __name__ == "__main__":
    build_features_and_train()
