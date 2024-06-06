Lenskart KPI Dashboard Project
This project aims to create a comprehensive Key Performance Indicator (KPI) dashboard for Lenskart, a leading eyewear retailer. The primary goal is to facilitate data-driven decision-making by providing visual insights into various aspects of Lenskart's operations, such as product performance, customer behavior, store efficiency, and transaction methods. The project leverages a combination of cloud technologies and business intelligence tools to achieve this.

Context and Objectives
Lenskart, like many modern retailers, generates a vast amount of data through its sales, customer interactions, and operational activities. Analyzing this data can provide valuable insights that help in strategic planning, operational improvements, and enhancing customer satisfaction. However, the challenge lies in collecting, processing, and visualizing this data in a way that is both efficient and user-friendly.

To address this, the Lenskart KPI Dashboard project was initiated with the following objectives:

Automated Data Collection: Develop a system to automatically collect data from Lenskart's API, ensuring that the data is up-to-date and comprehensive.
Robust Data Storage: Implement a scalable and secure data storage solution using Azure Blob Storage and Azure SQL Database to handle the collected data.
Data Processing and Transformation: Use Azure Data Factory to schedule and manage the transfer of data from Blob Storage to SQL Database, including necessary data transformations.
Interactive Data Visualization: Create a dynamic and interactive dashboard using Power BI to visualize key metrics, trends, and insights in a clear and actionable manner.
Project Components
Python: Scripts to fetch data from Lenskart API.
Azure Functions: Serverless computing to handle data collection triggers.
Azure Blob Storage: Intermediate storage for collected data.
Azure SQL Database: Centralized database for structured data storage.
Azure Data Factory: ETL service for data transfer and transformation.
Power BI: Visualization tool for creating interactive dashboards.
Data Collection
Data is collected from Lenskart's API using Python scripts. These scripts are scheduled to run periodically, triggered by Azure Functions, to ensure continuous data collection. The data is initially stored in Azure Blob Storage as a temporary holding area.

Data Storage and Processing
The collected data is transferred from Azure Blob Storage to Azure SQL Database using Azure Data Factory. This process involves setting up pipelines that define the workflow for data movement and transformation. The data is cleaned, transformed, and structured appropriately before being stored in the SQL database.

Data Visualization
Power BI is used to create the KPI dashboard. The dashboard includes various visual elements such as slicers, cards, charts, and matrices to provide a comprehensive view of the data. Key features of the dashboard include:

Metric Slicers: Allow users to filter and view data based on different metrics such as sales, quantity, and ratings.
Top Performers: Cards displaying the top product, customer, and store based on selected metrics.
Charts and Graphs: Visual representations of product performance, company performance over years, city performance, and payment methods.
Tooltips: Additional insights and details available on hover, including maps and detailed charts.
Conclusion
The Lenskart KPI Dashboard project integrates modern cloud services and data visualization tools to provide a powerful platform for data analysis and decision-making. By automating data collection, ensuring robust storage and processing, and creating interactive visualizations, the project aims to enhance Lenskart's ability to leverage its data for strategic insights and operational efficiency.
