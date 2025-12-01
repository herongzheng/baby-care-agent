# baby-care-agent
a baby-care agent that answers baby raising questions and manages daily events of your baby.

## Project setup:
To run this application, you need a Docker desktop on your device. In the file `baby-care_google_project/babycare_agent_app/.env`, fill in your Google API key for using Google LLMs.

Then, just run the the commands below to start interacting with this agent:

cd baby-care-agent/baby-care_google_project

>bring up MySQL service and the toolbox service, i.e. MCP server, in a detached mode

docker-compose up -d mysql toolbox

>once two services above are ready, run the application; enter **exit** if you want to quit the conversation with the agent

docker-compose run --rm python-app

>if you want to remove all resources created: containers, images, volumes and networks

docker-compose down --rmi all -v


## Example conversation
>>> Enter your message: My baby wakes up around 2 am, can you help me with that?

>>> User Query: My baby wakes up around 2 am, can you help me with that?
<<< Agent Response: "It's common for babies to wake up around 2 AM for a variety of reasons. These can include hunger, natural shifts in sleep cycles and developmental leaps (like the 4-month sleep regression), teething discomfort, environmental factors (too hot, too cold, dirty diaper), overtiredness, or simply a learned sleep association. It's recommended to ensure a comfortable sleep environment, maintain a consistent bedtime routine, and address any immediate needs like feeding or changing. If you have ongoing concerns, consulting with a pediatrician is advisable."

>>> Enter your message: What do you know about the pee records in year 2025?

>>> User Query: What do you know about the pee records in year 2025?
<<< Agent Response: I need more information to fulfill this request. Please provide the start and end dates for the time range you are interested in, including the year, month, and day.

>>> Enter your message: the entire year

>>> User Query: the entire year
<<< Agent Response: The pee records in the entire year 2025 are:
* Record_Id 2: Time: 2025-11-22 03:25:15, Amount: super, Normal: Yes
* Record_Id 3: Time: 2025-11-22 06:15:32, Amount: small, Normal: Yes
* Record_Id 1: Time: 2025-11-22 10:28:08, Amount: large, Normal: Yes

>>> Enter your message: Can you provide the pee records with volume large on date 2025 11.22?

>>> User Query: Can you provide the pee records with volume large on date 2025 11.22?
<<< Agent Response: On 2025-11-22, there was one record of a large volume pee. The record ID is 1, and it occurred at 10:28:08.


