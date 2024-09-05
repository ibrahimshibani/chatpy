# Description / Limitations / Future Developments
## Architecture
### Objects / Classes
1. **User**: Represents a user in the system (either a customer or an agent).
2. **Chat**: Represents an active chat session between a customer and an agent.
3. **Message**: Represents a message sent within a chat session.

### Interactions
- **User**: Can log in, start a chat session, and send messages.
- **Chat**: Manages the state of the chat, including participants and messages.
- **Message**: Contains the content of the message, sender information, and timestamp.

### Frontend Interaction
- The frontend interacts with the backend via RESTful API endpoints.
- Customers can log in, start a chat session, and send messages through a simple web interface.
- Agents can log in via another console (this can be emulated via curl or postman) and respond to customer messages.

## Quick Win Solution
The quick win solution is a basic implementation of a chat system that allows customers to send messages to customer service agents. This github repo is built only as a prototype for learning / poc purposes, it is definitely not ready for any type of prod. deployment. These points still need to be addressed for it to be considered a win or anywhere near deployment ready:

1. **Authentication**: 
    - **Current State**: The authentication mechanism is non-existent, and all data is transmitted in clear text. session ids are predictably generated and can be used to mimic users.
    - **Improvements**: implement secure authentication mechanisms such as OAuth or JWT. Encrypt data transmission using HTTPS to ensure that sensitive information is protected.

2. **Scalability**:
    - **Current State**: Although the app supports multiple sessions simultaneously, it will not scale well with increased load.
    - **Improvements**: Implement load balancing and horizontal scaling strategies. Optimize the backend to handle a higher number of concurrent users and messages efficiently.

3. **Database Technology**:
    - **Current State**: User credentials are stored in a JSON file, which is not suitable for production environments.
    - **Improvements**: Use an established database technology such as postgres,sql or mongodb for storing user credentials. These databases provide better security, reliability, and scalability.

4. **Session Data Storage**:
    - **Current State**: Session data is not stored efficiently.
    - **Improvements**: Use redis or mongoDB to store session/cache data. These technologies offer fast read/write operations and are better at working with live data, ensuring better performance and scalability.

5. **Frontend Technology**:
    - **Current State**: The current frontend is built using Streamlit, which is primarily designed for dashboarding and not for building interactive web applications.
    - **Improvements**: Develop a proper frontend using JavaScript or TypeScript with frameworks like React or Angular. 

6. **More Robust Data Validation**:
    - **Current State**: As the application grows in size, this means an increase in functionality and possible integrations (Mobile app, desktop app). The risk of unexpected input from users could cause unexpected errors and bad data eventually ending up in database.
    - **Improvements**: Utilize a tool like Pydantic (possible shifting to fastapi instead of flask as integrates more easily) which uses native python types like int or str to validate input to the system / database.
 
## State-of-the-Art Improvements (Icing on top of the cake)

I have a few improvements in mind which imo could make this really a top notch chat system:

1. **AI Integration**: Implement AI powered chatbots for automated responses and assistance. This can be done to relief pressure off of agents and prevent them from dealing with mundane tasks and focus on the use cases where customers require close assistance. This can be done in multiple ways,
    - for example a recommender system could be built using NLP technology that returns the relevant article if the user has questions about a product feature.
    - Train an llm either via prompt engineering or by fine-tuning with text data that could represent other interactions with customers, faq pages, product technical documentation etc etc.

2.  **WebSockets > HTTP (at least only in this use case)**
 as it allows for real time communication with instant data transfer and reduced latency since connections remain always open. i suspect this approach also reduces server load compared to HTTP and improves scalability by handling more users smoothly. 
 
3. **Kubernetes** Deploying the chat system on the cloud with Kubernetes offers benefits like auto-scaling which could cost saving, and load balancing, which distributes traffic evenly for better performance. 

4. **Observability** is crucial for gaining insights into the system's performance. By implementing telemetry/logging and metrics tracking, you can monitor performance and identify issues in real time. 
