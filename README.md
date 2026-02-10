AI-Supported Configuration Management System

## 1. Model Selection and Design Approach

In this project, a local language model was used to convert configuration requests written in natural language into a technical JSON format. **Phi-3** was chosen as the model and deployed locally via Ollama.

Main reasons for selecting this model:

- **Low hardware requirements:** Able to run stably on a MacBook M2  
- **Fast response time:** Eliminates network latency since it runs locally  
- **Consistent output generation:** Demonstrates sufficient performance in producing JSON in the desired format  

While designing the system, special attention was given to keeping the structure as simple and understandable as possible.

---

## 2. System Architecture

The application consists of four services launched via Docker Compose:

### Bot-Server
The main service that receives natural language commands from the user.  
It detects the relevant application, gathers the required data, and communicates with the model.

### Schema-Server
Provides valid JSON schemas for each service.  
This ensures that generated configurations are checked for the correct format.

### Values-Server
Reads existing configuration values and ensures that updated values are persistently written to files.

### Ollama (Phi-3)
The AI layer that converts natural language expressions into technical configuration parameters.

---

## 3. Request Flow

The end-to-end workflow of the system is as follows:

1. The user submits a configuration request in natural language.  
2. Bot-Server determines which application the request belongs to.  
3. The relevant schema and current value files are retrieved.  
4. This information is sent to the model along with the user request.  
5. The model generates the new configuration in JSON format.  
6. The generated JSON is validated against the schema.  
7. If validation succeeds, the values file is updated.  

This structure eliminates the need for manual JSON editing.

---

## 4. Test Scenarios

### Scenario 1 — Chat Service

**Command:**  
`set chat service maxUser to 150`

**System Response:**

```json
{
  "detected_app": "chat",
  "status": "success",
  "updated_config": {
    "maxUser": 150
  }
}
```

---

### Scenario 2 — Matchmaking Service

**Commdan:**  
`set matchmaking service waiting time to 3 minutes`

**System Response:**

```json
{
  "detected_app": "matchmaking",
  "status": "success",
  "updated_config": {
    "waitingTimeMinutes": 3
  }
}
```

---

### Scenario 3 — Tournament Service

**Commdand:**  
`tournament prize pool should be 5000`

**Sistem Response:**

```json
{
  "detected_app": "tournament",
  "status": "success",
  "updated_config": {
    "prizePool": 5000
  }
}
```

## 5. Overall Evaluation

The goal of this project is to enable users to update configurations using natural language without directly interacting with technical files.

The established architecture provides a structure that is:

- Simple  
- Scalable  
- Service-oriented  
- Locally deployable  

In future stages, the system can be further improved by increasing model accuracy and supporting a wider range of configuration parameters.
