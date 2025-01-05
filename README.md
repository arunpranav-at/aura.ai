<div>
<img src="assets\microsoft-removebg-preview.png" height="100" width="400" alt="Logo"/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="assets\azure-removebg-preview.png" height="100" width="300" alt="Logo" />
</div>

<center>
<h1 align="center">AURA - Analytics and Understanding for Responsible AI</h1>
</center>

AURA is an Azure AI based web application which is used to find hallucinations and ensure integrity among various AI models and LLMs along with confident scores, complete reasoning, detailed analytics and visualizations by comparing with external knowledge sources.
Multiple model support(gpt-4, gpt-4o, gpt-4o-mini, gpt-35-turbo-16k, etc.,), True and False negatives and positives, user friendly interface, detailed analytics, ready to use hosted platform are some of the unique selling points of our solution.
It is completely built on using Azure technologies like Azure App Service, Azure OpenAI, Bing Search API, Azure AI Evaluators, Azure Cosmos DB, Azure AI Foundry, Azure Container Registry, etc.,

<a href="" target="_blank">
  <img src="assets/www.png" height="50" width="50" alt="Website Logo" />
  To be added
</a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://github.com/arunpranav-at/aura.ai" target="_blank">
  <img src="assets/github.png" height="50" width="50" alt="GitHub Logo" />
</a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="" target="_blank">
  <img src="assets/youtube.png" height="50" width="50" alt="YouTube Logo" />
  To be added
</a>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href="" target="_blank">
  <img src="assets/ppt.jpeg" height="50" width="50" alt="Presentation Logo" />
  To be added
</a>
<br/><br/>

**Key Features:**
- Multiple model support (e.g., GPT-4, GPT-4o, GPT-4o-mini, GPT-35-Turbo-16k, and custom LLMs).
- User-friendly interface with hosted platform access.
- User accounts for storing chat history and detailed analytics for future references and contextual queries.
- Detailed analytics for AI evaluation metrics, including hallucination percentages.
- Confusion matrix showing true/false positives and negatives.
- Integration with Azure technologies for seamless scalability and reliability.


# **Table of Contents**

1. [Working](#working)
2. [Features](#features)
3. [Azure Technologies Used](#azure-technologies-used)
4. [Technologies Used](#technologies-used)
5. [Architecture](#architecture)
6. [Proposal](#proposal)
7. [Team Members](#team-members)
8. [Contributing](#contributing)
   - [Development](#development)
8. [License](#license)

# Working

AURA aims to be a robust framework and accessible service that identifies hallucinations in AI-generated outputs and validates them against trusted external data sources or a pre-defined knowledge base. Furthermore, it provides false positive and false negative rates for hallucination detection, with the ability to integrate and validate with multiple external knowledge sources, and provides user-friendly visualization of hallucination metrics.

# Features

- **Multi-Model Support**: Compare prominent LLMs like GPT-4, GPT-4o, and custom models.  
- **User Accounts:**: Support user account with authentication to maintain chat histories and user-specific analytics.  
- **Hallucination Analysis**: Detect hallucinations with reasoning and confidence scores for every output.  
- **Detailed Metrics**: Track performance using a confusion matrix and evaluator metrics like bias and violence detection.  
- **External Validation**: Validate results against trusted sources using Bing Search API.  


# Azure Technologies Used

Azure provides a robust ecosystem for development of services that can be deployed and integrated with ease. It supports integration through SDKs and libraries that aid in development of backend and continuous deployment respectively, improving development productivity while aiding in highly scalable and available deployments.

1. **Azure App Service:**
   
   Responsible for containerized deployment of frontend (Next.js application) and backend (FastAPI server) with Docker for efficiency in an automated manner using Github Actions, by leveraging Azure Container Registry.

2. **Azure Cosmos DB:**
   
   Used for storing user information for authentication, chat history, analytics and model test results by leveraging MongoDB for efficient querying and storage of large data for easier analytics and aggregation.

3. **Azure OpenAI:**
   
   Responsible for integration of multiple Azure-hosted GPT models for robust language understanding and output generation with API keys and endpoints for easier querying.

4. **Azure AI Foundry:**
   
   Aids in orchestration of multiple LLMs for efficient processing and endpoints for several LLMs that are provided by Azure OpenAI.

5. **Azure AI Service:**
   
   Enhances the application with pre-built AI capabilities like sentiment analysis and anomaly detection.

6. **Azure Bing Search API:**
   
   Serves as the primary source of extraction of information from external knowledge sources for validation of AI-generated content, which is used for verification of hallucination with and without context.

7. **Azure Container Registry:**
   
   Streamlines the deployment process by managing Docker containers for both the frontend and backend using continuous deployment for faster development to production environment.

8. **Azure SDK for Python:**
   
   Used for authentication to Azure services from backend and usage of AI Evaluator, that is responsible for detection of bias, violence, or other issues in AI outputs by using Azure OpenAI.

9. **Azure Cognitive Services:**
   
   Powers natural language understanding and computer vision features for enhanced analytics.


# Technologies Used

1. **Next.js**:

   Powers the frontend for a dynamic and responsive web application, by leveraging TailwindCSS for responsive design along with `react-chartjs` which is responsible for providing interactive and informative data visualizations of analytics.

2. **Python**:
   
   Serves as the backend's backbone for its simplicity and robust ecosystem, which allows
   seamless integration with libraries such as LangChain and Azure SDK for Python.

3. **FastAPI**:

   Enables rapid development of performant, asynchronous RESTful APIs with strong typing with Pydantic. Responsible for user authentication and integration with rest of Azure services along with the frontend

4. **MongoDB**:

   A NoSQL database for flexible and scalable data storage of user information, chat history and analytics, that is leveraged by Azure CosmosDB, using the `motor` library, which allows asynchronous processing, providing concurrency and better performance.

5. **GitHub**:
   
   Version control and collaboration for seamless development, with GitHub Actions that allows continuous deployment of frontend and backend to the production by leveraging Azure CLI and Docker.

6. **Docker**:

   Facilitates containerized application development and deployment for conflict-free and good developer experience. It is paired with Docker compose for multi-container orchestration, useful for local development

7. **LangChain**:

   Enhances the orchestration of multiple LLMs, that is used for response generation for the prompts given by the end-user, with or without context

# Architecture

![Architecture Diagram]()

## Frontend

The frontend of AURA is responsible for the following features:

1. **Authentication:**
   
   AURA supports unauthenticated users to test the platform and model without chat history,
   whereas authenticated users can access chat history which allows seamless access of chats.
   Thus AURA supports user account creation.

2. **Prompts to LLMs:**
   
   AURA supports prompting to several LLM models such as:
   - GPT-4
   - GPT-3.5-Turbo
   - GPT-4o
   - GPT-4o-mini

   based on requirements (in terms of accuracy) that are supported by the backend. This allows
   diversification of evaluation of hallucination in several models, helping in gathering
   analytics based on performance.
3. **Model testing:**

   AURA allows model testing by providing prompts with and without context that is processed 
   further by the backend and provides confusion matrix visualizations for better
   understanding.

4. **Analytics:**
   
   AURA provides an interactive dashboard, that provides visualizations based on several metrics such as hallucination, self-harm, sexual content, violence and hate unfairness.

## Backend

The backend of AURA is responsible for the following features:

1. **Authentication:**

   AURA's backend implements JWT based authentication for end-users for secure access, despite
   supporting unauthenticated access as it is meant to be an evaluation playground for several
   LLMs.

2. **Response generation:**

   The backend processes the prompts provided by the end-users and adds it to the chat history
   for authenticated users by integration with the chosen LLMs

3. **Hallucination evaluation by checking for groundedness:**

   Hallucination evaluation is done by leveraging Azure AI Evaluator, provided by Azure SDK for Python, which supports evaluation with and without context information, which helps in testing the groundedness of the models

4. **Context generation:**

   Context generation is done by leveraging external knowledge sources, primarily Bing API, for testing the models for groundedness by hallucinator evaluator

5. **Analytics:**
   
   Provides the needed information for the frontend for data visualization by querying from CosmosDB, which allows aggregated analysis
# Proposal

We propose to integrate our hallucinator predictor with Azure AI Studio for evaluation by integration of external data sources that can be used for validation of responses from models, which will be useful for enhancement of accuracy of LLMs over time through intensive analytics. This will be useful for monitoring performance metrics of LLMs provided by Azure AI Foundry, aiding in reduction of AI hallucinations present in early stages of adoption of AI

# Team Members

1. **Aruthra S**  
   - [GitHub](https://github.com/AruthraS)  
   - [LinkedIn](https://www.linkedin.com/in/aruthra-s-66b97b256/)  

2. **R S Kierthana**  
   - [GitHub](https://github.com/KierthanaRS)  
   - [LinkedIn](https://www.linkedin.com/in/kierthana-rajesh-8b8b42256/)  

3. **Arun Pranav A T**  
   - [GitHub](https://github.com/arunpranav-at)  
   - [LinkedIn](https://www.linkedin.com/in/arunpranavat/)  

4. **Keerthana R**  
   - [GitHub](https://github.com/grittypuffy)  
   - [LinkedIn](https://www.linkedin.com/in/keerthana304/)

# Contributing

We welcome contributions, expecially for improving our hallucination prediction and context generators, for building a robust ecosystem that aids in reduction of hallucinations in AI.
Contributions can involve feedback, reporting of bugs on our platform, documentation, design, code or infrastructure.

For contributing code or documentation, check below:

## Development

AURA is structured as a **monorepo**, organized as follows:

- **Frontend:** Built using Next.js for a dynamic and user-friendly web interface.
- **Backend:** RESTful APIs developed with Python and FastAPI.

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose for containerized development

### Steps to Run Locally

1. Verify Docker and Docker Compose are installed:
   ```shell
   docker -v
   docker compose version
   ```
2. Clone the repository and set up environment variables as per the `.env.sample` for the frontend and backend.
   ```shell
   git clone https://github.com/arunpranav-at/aura.ai
   cd aura.ai
   touch frontend/.env
   touch backend/.env
   ```
3. Build and start the services:
   ```shell
   docker compose --env-file frontend/.env --env-file backend/.env up --build
   ```

For more information regarding local development, check out the README for [frontend](/frontend/README.md) and [backend](/backend/README.md)


# License

AURA is licensed under MIT license, thus allowing permissive usage for your needs.