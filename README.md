# YouTube Analytics Project

<details>
  <summary><strong>Table of Contents</strong> (click to expand)</summary>

<!-- toc -->
- [Contributors](https://github.com/LHide14/YouTube-Analytics#Contributors)
- [Technologies](https://github.com/LHide14/YouTube-Analytics#Technologies)
- [What Makes a Good Data Science Video](https://github.com/LHide14/YouTube-Analytics#What-Makes-a-Good-Data-Science-YouTube-Video?)
- [Data Collection from YouTube API](https://github.com/LHide14/YouTube-Analytics#Data-Collection-from-YouTube-API)
- [Data Cleaning](https://github.com/LHide14/YouTube-Analytics#Data-Cleaning)
- [Exploratory Data Analysis part 1 - Key Findings](https://github.com/LHide14/YouTube-Analytics#Exploratory-Data-Analysis-part-1---Key-Findings)
- [Cloud Automated ETL Pipeline](https://github.com/LHide14/YouTube-Analytics#Cloud-Automated-ETL-Pipeline)
- [Exploratory Data Ananlysis part 2](https://github.com/LHide14/YouTube-Analytics#Exploratory-Data-Ananlysis-part-2)
- [Machine Learning and Modelling](https://github.com/LHide14/YouTube-Analytics#Machine-Learning-and-Modelling)
<!-- tocstop -->
</details>

## Contributors

**Lawrence**

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/LHide14)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lawrence-hide-417255144/)

**Mo**

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/mms-mirza)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mms-mirza/)

## Technologies

<table align='float:left;'>
    <tr>
        <td align='center'><img width="70" src="https://github.com/LHide14/LHide14/blob/main/python.png" title="python"></td>
        <td align='center'><img width="70" src="https://github.com/LHide14/LHide14/blob/main/jupyter.png" title="jupyter"></td>
        <td align='center'><img width="70" src="https://github.com/LHide14/LHide14/blob/main/pandas.png" title="pandas"></td>
        <td align='center'><img width="70" src="https://github.com/LHide14/LHide14/blob/main/numpy.png" title="numpy"></td>
    </tr>
    <tr>
        <td align='center'><img width="70" src="https://github.com/LHide14/LHide14/blob/main/2560px-Scikit_learn_logo_small.svg.png" title="sklearn"></td>
        <td align='center'><img width="70" src="https://github.com/LHide14/LHide14/blob/main/github.png" title="github"></td>
        <td align='center'><img width="70" src="https://github.com/LHide14/LHide14/blob/main/icons8-google-cloud-50.png" title="GCP"></td>
    </tr>
</table>  

## What Makes a Good Data Science YouTube Video?

YouTube is the largest video sharing platform in world, with billions of views everyday. This gives it the ability to support thousands of creators across a range of subjects, including Data Science. Furthermore, the platform has become a fertile ground for business marketting; including advertising on videos, partneships and sponsorships with channels, or allowing business' to host their own video adverts.

### Business Case:
- Understanding which videos to prioritise for marketting spending
- Maximising monetisation and sponsorship opportunities in video production
- Increasing educational reach of Data Science videos

### Project Flow:


```mermaid
flowchart LR;
  A{{Collect data from YouTube API}} --> B{{Data Cleaning}} --> C{{EDA}} --> D{{Cloud Automated ETL Pipeline}} --> E{{EDA on Pipeline}} --> F{{Modelling}};
```

## Data Collection from YouTube API

### API Connection:
We created a Google Account to access the Google API Console, then created a project in the Develeopers Console, and enabled YouTube Data API v3 to request an API key.

### JSON Request to Data Frame Flow:
```mermaid
flowchart TD;
  A{{Manual selection and collection of Channel IDs}} --> B{{Function to collect Channel Stats}} --> C{{Filtering Channels}} --> D{{Function to collect video IDs}} --> E{{Function to collect Video Stats}};
  B --> G[(Channel Data Frame)];
  E --> H[(Video Stats Data Frame)];
  G --> I[\Merge/];
  H --> I[\Merge/];
  I --> F[(Final Data Frame)]
```

## Data Cleaning

### Cleaning Flow:
```mermaid
flowchart TD;
  A{{Handling Null Values}} --> B{{Check for Duplicates}} --> C{{Change Data Types}} --> D{{Altering Columns}} --> E{{Creating Columns}} --> F{{Dropping Columns}} --> G[(Clean Data Frame)];
```

### Target Column:
The Target Column, was created by splitting from the median view count of 6856. With 1 being video views greater than the median, and 0 being video views less than the median.

We chose this categorisation to determine what classes as a 'good video' or 'bad video' in our data, because those in the '1' category will always have more views than 50% of all other Data Science videos.

## Exploratory Data Analysis part 1 - Key Findings
<img src="https://github.com/LHide14/YouTube-Analytics/blob/main/README_visualisations/viewcount_distribution.png">
<img src="https://github.com/LHide14/YouTube-Analytics/blob/main/README_visualisations/category_distribution.png">
<img src="https://github.com/LHide14/YouTube-Analytics/blob/main/README_visualisations/toptags_distribution.png">
<img src="https://github.com/LHide14/YouTube-Analytics/blob/main/README_visualisations/subscribersVSviewcount.png">
<img src="https://github.com/LHide14/YouTube-Analytics/blob/main/README_visualisations/nooftagsVSviewcount.png">
<img src="https://github.com/LHide14/YouTube-Analytics/blob/main/README_visualisations/licensedcontentVStarget.png">
<img src="https://github.com/LHide14/YouTube-Analytics/blob/main/README_visualisations/channelVStarget_percentage.png">

## GCP Automated ETL Pipeline
```mermaid
flowchart TD;
  A{{Cloud Scheduler}} -- Triggers --> B{{Pub/Sub}} -- Messages --> C{{Cloud Function 1st gen}} -- Script Executes --> D[(Cloud Storage Bucket)] --> E[\"Transform:
  Time Delta Column
  Merge Data Frames
  Eliminate Excess Data
  Flip Rows"/] --> F[(Final Data Frame)] ;
``` 

## Machine Learning and Modelling
```mermaid
flowchart TD;
  A[(Data)] --> B[(Numerical Data)] --> C{{Random Forest Classifier}} --> D{{Ensemble Model}};
  A --> E[(Text Data)];
  E --> F[(Title Data)];
  E --> G[(Description Data)];
  F --> H{{Logistic Regression Model}};
  G --> I{{Logistic Regression Model}};
  H --> D{{Ensemble Model}};
  I --> D{{Ensemble Model}}
```
