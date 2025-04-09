## Generic Property Demo
An AI pipeline using synthetic data to demonstrate different use cases. The purpose of this is for us to be able showcase the demo to potential clients without breaking NDA.

This demo is aimed to be reusable for other domain eg property_agent. Hence, the generice focused use cases.

## Technology Stacks
* Python 3.12
* CrewAI
* Watsonx.ai
* React
* Vite


### How-to-run-this-demo
The following are the steps for you to get this demo up and running. We assume you already have an environment reserved. If not you can proceed to reserving an env in [TechZone](https://techzone.ibm.com/collection/technology-patterns/journey-ai-assistants) with ES, Wx.Ai and Wx Assistant as part of the component

-----------------------------
  
#### Front End  
  
From root go to frontend dir
```
cd front-end
```
For first time running:
```
npm install
```
  
To run the app:
```
npm run dev
```

To run front-end as image
```
podman build -t property_agent_fe .
podman run --name property_agent_fe --rm -p 8080:8080 property_agent_fe
```

#### Back End
  
From root go to backend/property_agent dir
```
cd back-end/property_agent
```

To initialize crewai
```
crewai install
source .venv/bin/activate
```
  
To test crewai locally
```
uv run kickoff
```
or 
```
python src/property_agent/main.py
```

To run fast api
```
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

To run back-end as image
```
podman build -t property_agent_be .
podman run --name property_agent_be --rm -p 8080:8080 property_agent_be
```