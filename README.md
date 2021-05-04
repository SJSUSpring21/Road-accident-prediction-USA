# Road accident data analysis and Severity Prediction


### Abstract :
In this project, we set out to solve the problem of Road Traffic Accident(RTA) in USA  by providing a tool to predict RTA risk so that users can make informed decision about their traveling route. We also did a detailed analysis of past data and visuals to gain a better understanding of RTA.This application would offer the severity of accident at given locations based on factors such as weather, time of day, etc. using the US Accidents dataset.We would offer drivers with a dashboard where they can look up the accident rate for a city,
by leveraging this historical dataset. Traffic control authorities can also benefit from the hotspot accident locations
featured in the application dashboard.

Our web interface contains two parts, namely exploration and interaction. In the exploration part, we presents our research methodology, algorithm used, analysis and visualization of the data. In the interaction part, user can make use of an interactive dashboard to predict the probability of RTA in their chosen routes.

The app uses machine learning models for predictions. User will have to enter the destination. The app will then call Google maps API for route planning and a weather API (openweathermap.org) for finding the weather conditions as well as date and time of the location.

**(Add-on)** We would like to use this dataset to study the impact of COVID-19 on traffic behavior and accidents.


### Technologies used :

* Front-end : React JS
* Back- end : Python 


### Approach :
Analyze the dataset to create dashboards to understand traffic distributions in cities.
Use the below classification algorithms to predict the probability of accidents.
* Logistic Regression 
* Decision Tree
* Random Forest
* KNN (k- nearest neighbors)

Choose the model which produces the most accuracy, precision and recall.

In Our application we have finalized to use Random Forest by comparing with other models mentioned.

### Persona :
1. Travelers and drivers to choose safest routes
2. Traffic control authorities to find the most accident prone areas and take required actions.


### Dataset : 
The dataset consists of traffic data captured by a variety of entities such as the US and State departments
of transportation, law enforcement agencies, traffic cameras, and traffic sensors within the road-networks.

### Architectural Diagram
![Program Architecture](https://user-images.githubusercontent.com/78836467/110733016-1465c680-81da-11eb-8a23-13cafb18807d.jpg)

