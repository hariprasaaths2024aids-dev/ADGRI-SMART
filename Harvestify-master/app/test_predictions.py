import pickle
import numpy as np
import pandas as pd
import os

# Load the crop recommendation model
model_path = os.path.join(os.path.dirname(__file__), 'models', 'RandomForest.pkl')
crop_model = pickle.load(open(model_path, 'rb'))

print("=" * 80)
print("🌾 CROP RECOMMENDATION TESTS")
print("=" * 80)

# Test Case 1: Rice (typical values for rice cultivation)
test1 = np.array([[90, 42, 43, 6.5, 20.8, 82.0, 202.9]])
result1 = crop_model.predict(test1)
print(f"\n✅ Test 1 - Rice Growing Conditions:")
print(f"   N=90, P=42, K=43, pH=6.5, Temp=20.8°C, Humidity=82%, Rainfall=202.9mm")
print(f"   Prediction: {result1[0].upper()}")

# Test Case 2: Coffee (typical values for coffee)
test2 = np.array([[100, 80, 30, 6.5, 23.0, 65.0, 150.0]])
result2 = crop_model.predict(test2)
print(f"\n✅ Test 2 - Coffee Growing Conditions:")
print(f"   N=100, P=80, K=30, pH=6.5, Temp=23°C, Humidity=65%, Rainfall=150mm")
print(f"   Prediction: {result2[0].upper()}")

# Test Case 3: Wheat (typical values for wheat)
test3 = np.array([[50, 30, 20, 6.8, 15.0, 55.0, 60.0]])
result3 = crop_model.predict(test3)
print(f"\n✅ Test 3 - Wheat Growing Conditions:")
print(f"   N=50, P=30, K=20, pH=6.8, Temp=15°C, Humidity=55%, Rainfall=60mm")
print(f"   Prediction: {result3[0].upper()}")

print("\n" + "=" * 80)
print("🧪 FERTILIZER RECOMMENDATION TEST")
print("=" * 80)

# Load fertilizer data
fertilizer_df = pd.read_csv('Data/fertilizer.csv')

# Test Case: High Nitrogen for Rice
print(f"\n✅ Test - Rice with N=120, P=42, K=43 (High Nitrogen)")
crop = 'rice'
N = 120  # High
P = 42   # Normal
K = 43   # Normal

# Find average NPK for rice
crop_data = fertilizer_df[fertilizer_df['Crop'] == crop]
if not crop_data.empty:
    nr = crop_data['N'].iloc[0]
    pr = crop_data['P'].iloc[0]
    kr = crop_data['K'].iloc[0]
    
    print(f"   Expected NPK for rice: N={nr}, P={pr}, K={kr}")
    print(f"   Your soil: N={N}, P={P}, K={K}")
    
    n_diff = N - nr
    p_diff = P - pr
    k_diff = K - kr
    
    recommendations = []
    if n_diff > 0:
        recommendations.append(f"Nitrogen is HIGH (+{n_diff})")
    elif n_diff < 0:
        recommendations.append(f"Nitrogen is LOW ({n_diff})")
    else:
        recommendations.append("Nitrogen is OPTIMAL")
        
    if p_diff > 0:
        recommendations.append(f"Phosphorous is HIGH (+{p_diff})")
    elif p_diff < 0:
        recommendations.append(f"Phosphorous is LOW ({p_diff})")
    else:
        recommendations.append("Phosphorous is OPTIMAL")
        
    if k_diff > 0:
        recommendations.append(f"Potassium is HIGH (+{k_diff})")
    elif k_diff < 0:
        recommendations.append(f"Potassium is LOW ({k_diff})")
    else:
        recommendations.append("Potassium is OPTIMAL")
    
    print("\n   Recommendations:")
    for rec in recommendations:
        print(f"   • {rec}")

print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETED!")
print("=" * 80)
