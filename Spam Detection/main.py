from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd
import re

def load_data():
    # Load the dataset
    data = pd.read_csv('spam.csv', encoding='ISO-8859-1')

    # Check if 'text' and 'label' columns exist
    if 'text' not in data.columns or 'label' not in data.columns:
        raise ValueError("Dataset must contain 'text' and 'label' columns")

    # Map the labels to 0 for ham and 1 for spam
    data['label'] = data['label'].map({'ham': 0, 'spam': 1})

    # Clean the text data by removing digits and non-word characters
    data['text'] = data['text'].replace(r'\d+', '', regex=True)  # Remove numbers
    data['text'] = data['text'].replace(r'\W+', ' ', regex=True)  # Remove non-word chars

    return data

def vectorize_data(data):
    # Initialize the TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english')  # Optional: Remove common stop words
    vectorized_data = vectorizer.fit_transform(data['text'])
    return vectorized_data, vectorizer

def test_new_data(new_data, model, vectorizer):
    # Preprocess each new email (remove digits and non-word characters using re.sub)
    new_data_cleaned = [re.sub(r'\d+', '', email) for email in new_data]  # Remove digits
    new_data_cleaned = [re.sub(r'\W+', ' ', email) for email in new_data_cleaned]  # Remove non-word chars

    # Vectorize the cleaned data
    new_data_vectorized = vectorizer.transform(new_data_cleaned)

    # Make predictions on the new data
    predictions = model.predict(new_data_vectorized)
    
    # Output the results
    print("\nTesting new emails:")
    for text, prediction in zip(new_data, predictions):
        print(f"Text: {text}")
        print(f"Prediction: {'Spam' if prediction == 1 else 'Ham'}\n")

def main():
    # Load and preprocess the data
    data = load_data()

    # Vectorize the data
    vectorized_data, vectorizer = vectorize_data(data)

    # Split the data into training and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(vectorized_data, data['label'], test_size=0.2, random_state=42)

    # Initialize the Naive Bayes classifier
    model = MultinomialNB()
    cross_val_score(model, vectorized_data, data['label'], cv=5).mean()

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")

    # Print confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)

    new_emails = [
    "Win a free iPhone! Call now for a prize!",
    "Hey, are we still meeting tomorrow for coffee?",
    "Get 50% off your next purchase!",
    "Reminder: Your appointment is scheduled for next week.",
    "Can you send me the report by end of day?"
    ]

    test_new_data(new_emails, model, vectorizer)

# Run the main function
if __name__ == "__main__":
    main()
