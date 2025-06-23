```mermaid
graph TD
    %% Nodes
    User[Usuario] -->|Consultas| ChatInterface
    ChatInterface --> ChatLogic[chat.py]
    ChatLogic[chat.py] -->|Procesamiento API| AIAssistant[Asistente IA]
    AIAssistant[Asistente IA] --> EntryPoint[main.py]
    EntryPoint[main.py] --> AILogic[ai/chat.py]
    AILogic[ai/chat.py] --> AppConfig[config.py]
    AILogic[ai/chat.py] --> VectorProcessor[vector.py]
    AILogic[ai/chat.py] --> SQLModule[sql.py]
    AILogic[ai/chat.py] -->|Preparación de Recomenciones y Chat Conversacional| OpenAI[GPT4o]

    %% Subgraphs
    subgraph Aplicación Principal
        ChatInterface
        AIAssistant
        EntryPoint[main.py]
        AppConfig[config.py]
    end

    subgraph Componentes de Datos
        SQLModule[sql.py]
        VectorProcessor[vector.py]
    end

    subgraph Modelos IA
        OpenAI[GPT4o]
    end

    %% Database Details
    SQLModule[sql.py] -->|Información Nutricional| Config[base_grupo8.db]
    VectorProcessor[vector.py] -->|Historial y Feedback| Confíg[base_vectorial_Redis]


    %% Deployment
    subgraph Despliegue
        Heroku[Heroku]
        Procfile[Procfile]
        Runtime[runtime.txt]
    end

    %% Styling
    classDef default fill:#ffffff,stroke:#333333,stroke-width:2px,color:#000000
    classDef primary fill:#e6f0ff,stroke:#003366,stroke-width:2px,color:#000000
    classDef data fill:#e6ffe6,stroke:#006600,stroke-width:2px,color:#000000
    classDef deployment fill:#e6e6ff,stroke:#000080,stroke-width:2px,color:#000000
    classDef model fill:#fff0e6,stroke:#cc6600,stroke-width:2px,color:#000000

    class User,ChatInterface,AIAssistant,EntryPoint,AppConfig primary
    class SQLModule,VectorProcessor data
    class Heroku,Procfile,Runtime deployment

    %% Legend
    subgraph Leyenda
        direction TB
        Primary[Componentes Principales]
        Data[Componentes de Datos]
        Deployment[Componentes de Despliegue]
    end

    class Primary primary
    class Data data
    class Deployment deployment

    %% Connections
    style User fill:#ffffff,stroke:#333333,stroke-width:3px,color:#000000
```
