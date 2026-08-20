\# Fraud SMS Classifier



A machine learning web app that detects fraudulent SMS messages targeting Nigerians — fake bank alerts, BVN/KYC scams, lottery scams, fake job offers, and more.



Built as a capstone project for the 3MTT NextGen AI \& ML Programme.



\## Problem



Nigerians are frequently targeted by SMS scams: fake bank debit alerts, fake POS notifications, "you have won" lottery scams, phishing links posing as bank security updates, fake BVN/NIN/KYC verification requests, fake investment schemes, and fake job offers. This project uses machine learning to automatically flag suspicious messages, giving users a quick way to check an SMS before acting on it.



\## What It Does



\- Accepts a pasted SMS message

\- Classifies it as Fraud/Spam or Safe/Legitimate

\- Shows a confidence score for the prediction

\- Highlights suspicious keywords found in the message (e.g. BVN, OTP, "click", "urgent")

\- Displays the cleaned text used internally for the prediction



\## Dataset



\- UCI SMS Spam Collection (5,572 messages, ham/spam labeled)

\- Supplemented with 31 manually written Nigerian-context examples (fake bank alerts, BVN/KYC scams, lottery scams, fake job offers, and corresponding safe messages)

\- After removing 403 duplicate entries: 5,200 messages (4,532 ham / 668 spam)



\## Approach



1\. Data cleaning: lowercasing, URL/HTML removal, punctuation/number removal, stopword removal, lemmatization (NLTK)

2\. Feature engineering: TF-IDF vectorization (3,000 features)

3\. Model comparison: Naive Bayes, Logistic Regression, and Linear SVM were trained and evaluated

4\. Best model: Linear SVM was selected based on the strongest F1-score and recall



\## Results



Model comparison (test set of 1,040 messages):



\- Naive Bayes: Accuracy 96.44%, Precision 98.02%, Recall 73.88%, F1-score 84.26%

\- Logistic Regression: Accuracy 94.42%, Precision 97.50%, Recall 58.21%, F1-score 72.90%

\- Linear SVM (selected): Accuracy 97.40%, Precision 97.35%, Recall 82.09%, F1-score 89.07%



Confusion Matrix (Linear SVM):



\- Actual Ham, Predicted Ham: 903

\- Actual Ham, Predicted Spam: 3

\- Actual Spam, Predicted Ham: 24

\- Actual Spam, Predicted Spam: 110



\## Error Analysis



\- False negatives (missed spam) were mostly adult-content spam and UK premium-SMS spam — categories linguistically different from the Nigerian fraud patterns this project targets.

\- False positives (safe messages flagged as spam) were messages that stylistically resembled scams — e.g. job-offer language or messages containing links — a reasonable trade-off for a cautious fraud detector.



\## Tech Stack



\- Python, pandas, NumPy, scikit-learn, NLTK, Matplotlib

\- Streamlit (web app)

\- Joblib (model persistence)



\## How to Run Locally



1\. Clone or download this repository

2\. Install dependencies:

&#x20;  pip install -r requirements.txt

3\. Run the app:

&#x20;  streamlit run app.py

4\. Your browser will open automatically at http://localhost:8501



\## Project Structure



Fraud\_SMS\_Classifier/

\- app.py (Streamlit web application)

\- requirements.txt (Python dependencies)

\- models/

&#x20; - fraud\_sms\_model.pkl (Trained Linear SVM model)

&#x20; - tfidf\_vectorizer.pkl (Fitted TF-IDF vectorizer)

\- notebooks/

&#x20; - Fraud\_SMS\_Classifier.ipynb (Full training notebook: EDA, cleaning, training, evaluation)

\- data/ (Dataset files)

\- screenshots/ (App screenshots)

\- README.md



\## Future Improvements



\- Expand the Nigerian-context training examples for better local coverage

\- Add multilingual support (Pidgin English)

\- Deploy the app publicly (e.g. Streamlit Community Cloud)

\- Add a feedback mechanism so users can report misclassifications to improve the model over time



\## Author



Isa Haruna Aliyu

3MTT NextGen AI \& ML Programme

BSc.(Ed.)(Hons.) Computer Science , Gombe State University



\## License



This project was built for educational purposes as part of the 3MTT NextGen AI \& ML Capstone Project.

