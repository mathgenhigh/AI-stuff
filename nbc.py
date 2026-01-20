import pandas as pd 

# Define dataset
data = {
    'ID' : [1, 2, 3, 4, 5, 6],
    'Age': ['Young', 'Young', 'Middle', 'Middle', 'Old', 'Old'],
    'Income': ['High', 'Low', 'High', 'Low', 'High', 'Low'],
    'Buy': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No']
}

df = pd.DataFrame(data)
print(f"Dataset:\n{df}\n")

# Calculate priors
total = len(df)
prior_yes = len(df[df['Buy'] == 'Yes']) / total
prior_no = len(df[df['Buy'] == 'No']) / total
print(f"P(Yes) = {prior_yes}")
print(f"P(No) = {prior_no}\n")

# Calculate likelihoods
def likelihood(feature, value, target_value):
    subset = df[df['Buy'] == target_value]
    return len(subset[subset[feature] == value]) / len(subset)

features = ['Age', 'Income']
classes = ['Yes', 'No']

likelihoods = {}
for f in features:
    likelihoods[f] = {}
    for val in df[f].unique():
        likelihoods[f][val] = {}
        for cl in classes:
            likelihoods[f][val][cl] = likelihood(f, val, cl)

# Print likelihoods
print("Likelihoods: ")
for f in likelihoods:
    for val in likelihoods[f]:
        print(f"{f}={val} | Yes: {likelihoods[f][val]['Yes']:.3f}, No: {likelihoods[f][val]['No']:.3f}\n")

# Predict function
def predict(input_data):
    prob_yes = prior_yes
    prob_no = prior_no 
    for f, val in input_data.items():
        prob_yes *= likelihoods[f][val]['Yes']
        prob_no *= likelihoods[f][val]['No']
    prediction = 'Yes' if prob_yes > prob_no else 'No'
    return prediction, prob_yes, prob_no

# Test examples
test_examples = [
    {'Age': 'Middle', 'Income': 'High'},
    {'Age': 'Old', 'Income': 'Low'}
]

for i, example in enumerate(test_examples, 1):
    pred, p_yes, p_no = predict(example)
    print(f"Test example {i}: {example}")
    print(f"P(Yes) = {p_yes:.3f}, P(No) = {p_no:.3f} -> Prediction: {pred}\n")