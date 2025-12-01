# baby-care-agent
a baby-care agent that answers baby raising questions and manages daily events of your baby

Project setup:
To run this application, you need a Docker desktop on your device. Then, just run the the commands below to start interacting with this agent

cd baby-care-agent

# bring up MySQL service and the toolbox service, i.e. MCP server, in a detached mode
docker-compose up -d mysql toolbox

# when above two services are ready, bring run the application; enter exit if you want to quit the conversation
docker-compose run --rm python-app

# if you want to remove all resources created: containers, images, volumes and networks
docker-compose down --rmi all -v


