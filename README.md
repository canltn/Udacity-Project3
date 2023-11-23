# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| Azure Postgres Database | Basic - Single Server | 50.14 USD |
| Azure Service Bus | Basic Service Plan - B1 | 0.05 USD|
| Azure Functions | Consumption Tier |...|
| Storage Accounts | Storage (general purpose v1)| ...   |
## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.
# Udacity-Project3
Azure Web App:
1. App Type:

Monolithic Applications: If your application is monolithic and doesn't have a need for microservices architecture, a standard Azure Web App might be suitable.
Microservices: For more complex applications with a microservices architecture, consider breaking down the functionalities into separate services, and deploy each as a separate Azure Web App.
2. Scalability:

Vertical Scaling: If your application can be scaled vertically (by adding more resources to a single instance), Azure Web App can handle this well.
Horizontal Scaling: For applications that require horizontal scaling (adding more instances of the application), Azure Web App's built-in load balancing and auto-scaling features are beneficial.
3. Managed Services vs. Customization:

Managed Services: If you prefer a fully managed environment with less infrastructure management, Azure Web App provides a platform that abstracts away the underlying infrastructure details.
Customization: If you need more control over the underlying infrastructure (like installing custom software or configuring advanced networking settings), you might consider other Azure services like Azure Virtual Machines.
4. Development Stack:

Built-in Stacks: Azure Web App supports various built-in stacks for different programming languages and frameworks. Choose the stack that aligns with your development preferences.
Azure Function:
5. Event-Driven Architecture:

Event-Driven Applications: Azure Functions are well-suited for event-driven architectures. If your application involves reacting to events or triggers (e.g., HTTP requests, message queues, timers), Azure Functions can be a good fit.
6. Serverless Architecture:

Serverless: If you want to leverage a serverless architecture, where you pay only for the actual compute resources used, Azure Functions is a strong choice. It automatically scales based on demand.
7. Stateless Operations:

Stateless Functions: Azure Functions are designed to be stateless, meaning they're well-suited for short-lived operations that don't require maintaining state between function executions.
8. Integration with Other Azure Services:

Integration Points: Azure Functions seamlessly integrates with other Azure services. If your application relies on various Azure services, Azure Functions can be used to glue different components together.
9. Microservices:

Microservices Architecture: If your application follows a microservices architecture, you can deploy individual functions to handle specific microservices tasks, allowing for a modular and scalable approach.
In summary, the choice of architecture for Azure Web App and Azure Function depends on your specific application requirements, development preferences, and scalability needs. It's often beneficial to mix and match these services based on the distinct characteristics of your application components.