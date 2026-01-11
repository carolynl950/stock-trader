# System Architecture

Users upload Python trading strategies to Firebase Storage.
A Flask backend retrieves and executes the latest script per user.
Results are stored in Firebase Firestore and visualized via FlutterFlow.