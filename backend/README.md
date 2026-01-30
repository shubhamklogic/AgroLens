# Backend Module – AgroLens

This folder contains the backend logic of the AgroLens application.

The backend is responsible for:
- Handling application logic
- Managing REST APIs
- Processing user input
- Connecting the machine learning model with the mobile app
- Supporting offline functionality using a local server

## Responsibilities
- Backend and API development
- Data handling and validation
- Machine learning model integration
- Offline backend support

## Technologies Used
- Python
- Flask (Local REST API)
- JSON-based API communication

### Progress Update: 18/01/26
- Successfully initialized Flask server.
- Created root route ("/") returning a status message.
- Tested local server connection on port 5000.

### Progress Update: 19/01/26
- **API Endpoint Created**: Implemented the `/predict` route.
- **JSON Integration**: Utilized `jsonify` to return structured data instead of plain text.
- **Data Standardization**: Defined a standard response format containing `crop`, `yield_prediction`, and `status` to ensure compatibility with the mobile frontend.

## Maintained By
Shubham (Backend & API Engineer)
