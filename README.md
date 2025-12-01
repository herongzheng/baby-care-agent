# baby-care-agent
a baby-care agent that answers baby raising questions and manages daily events of your baby

## Project setup:
To run this application, you need a Docker desktop on your device. In the file `baby-care_google_project/babycare_agent_app/.env`, fill in your Google API key for using Google LLMs.

Then, just run the the commands below to start interacting with this agent

cd baby-care_google_project

**bring up MySQL service and the toolbox service, i.e. MCP server, in a detached mode**
docker-compose up -d mysql toolbox

**when above two services are ready, bring run the application; enter exit if you want to quit the conversation**
docker-compose run --rm python-app

**if you want to remove all resources created: containers, images, volumes and networks**
docker-compose down --rmi all -v


