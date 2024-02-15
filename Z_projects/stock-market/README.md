# Stock Market Data Web Application

- [Stock Market Data Web Application](#stock-market-data-web-application)
	- [Overview](#overview)
	- [Implemented Functionalities](#implemented-functionalities)
	- [Additional Functionalities Implemented](#additional-functionalities-implemented)
	- [Repository Structure](#repository-structure)
	- [Lessons Learned](#lessons-learned)
		- [Data Visualization Part](#data-visualization-part)
		- [Deployment to Render](#deployment-to-render)
		- [Customizing Generic Views](#customizing-generic-views)


## Overview

This web application is built using Python and Django framework to visualize stock market data. It provides functionalities to view, edit, create, and delete stock market data records. Additionally, it includes interactive chart visualizations for better analysis.

## Implemented Functionalities

1. **Table Visualization:** Displays stock market data in a tabular format on the home page.
2. **Editable Rows/CRUD Functionality:** Allows users to perform CRUD (Create, Read, Update, Delete) operations on stock market data records. Among them create, update, and delete operations are protected by user authentication.
3. **Multi-axis Chart:** Accommodates both line and bar chart visualizations together with the 'close' column represented in the line chart and the 'volume' column in the bar chart.
4. **Dropdown Selection:** Includes a dropdown menu in the chart to choose the 'trade_code' column, which updates the data in the line chart.

## Additional Functionalities Implemented

- **Additional Visualization:** Incorporates a **candlestick chart** for stock market data visualization, offering additional insights into the market trends.
- **Dark Mode Support:** Includes support for dark mode, allowing users to switch between light and dark themes for better viewing experience.
- **User Authentication:** Implements user authentication using Django's built-in authentication system to secure CRUD operations and access control.
- **Pagination:** Implements pagination for better navigation and performance, ensuring smooth user experience even with large datasets.
- **Session Management:** Uses session management to store user preferences, such as dark mode setting, across different pages.

## Repository Structure

The project repository is organized into the following directories:

- **stockview:** Contains Django app files, including models, views, templates, and static files.
- **stockview\scripts\run_seed.py:** Script to seed the SQL database with stock market data from the provided JSON file. Command to run the script: `python manage.py runscript run_seed`.


## Lessons Learned

### Data Visualization Part

- **Understanding Plotly:** Through this project, I gained a deeper understanding of Plotly, a powerful Python library for creating interactive and dynamic visualizations. I learned how to leverage Plotly's capabilities to generate various types of charts, including **candlestick** charts, and how to customize these visualizations to meet specific requirements.
- **Multi-axis Charts:** Implementing multi-axis charts was a valuable learning experience. I learned how to combine multiple traces with different scales (e.g., price and volume) into a single chart, allowing for better analysis and comparison of different data series.
- **Dynamic Chart Updates:** Adding dynamic dropdown selection to update the chart based on user input enhanced my understanding of how to create interactive visualizations that respond to user actions. This feature enables users to customize their analysis by selecting specific data categories or attributes.

### Deployment to Render

- **Deployment Challenges:** Deploying the web application to Render posed several challenges, including setting up the environment, configuring the database, and managing static files. I learned how to troubleshoot deployment issues, optimize performance, and ensure the application runs smoothly in a production environment.
- **Static Files Management:** Understanding the importance of properly managing static files (e.g., CSS, JavaScript) in a Django project was crucial for successful deployment. I learned how to configure Django settings to serve static files efficiently and how to handle versioning and caching to improve performance.
- **Database Configuration:** Configuring the database settings for deployment required careful consideration of factors such as scalability, performance, and security. I learned how to choose the appropriate database provider, set up database connections, and manage database migrations to ensure data integrity and reliability in a production environment.

### Customizing Generic Views

- **Understanding Generic Views:** I delved into the details of Django's generic views and learned how to customize them to suit specific project requirements. This included customizing ListView, CreateView, UpdateView, and DeleteView to implement CRUD functionalities for stock market data records.
- **Adding Custom Functionality:** By customizing generic views, I was able to add additional functionalities such as dynamic chart updates, user authentication, and input date picker widgets. This allowed me to tailor the views to meet the project's needs while maintaining code reusability and consistency.
- **Optimizing Performance:** I learned techniques for optimizing the performance of generic views, such as pagination and queryset optimization. These optimizations ensured smooth performance, even when dealing with large datasets, and enhanced the overall user experience.

Overall, this project provided me with valuable insights into data visualization techniques, deployment best practices, and customizing generic views in Django. It equipped me with the skills and knowledge necessary to build robust web applications that effectively visualize and analyze data while adhering to best practices in web development.