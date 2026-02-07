import pickle
import pandas as pd

# Load the preprocessor
with open('artifacts/preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

# Check what the preprocessor expects
print("=" * 80)
print("PREPROCESSOR CONFIGURATION")
print("=" * 80)

for name, transformer, columns in preprocessor.transformers_:
    print(f"\nTransformer: {name}")
    print(f"Columns: {columns}")
    print(f"Transformer type: {type(transformer)}")
    
    # Check if it's a Pipeline
    if hasattr(transformer, 'steps'):
        print("Pipeline steps:")
        for step_name, step_transformer in transformer.steps:
            print(f"  - {step_name}: {type(step_transformer)}")

print("\n" + "=" * 80)