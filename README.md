# Recommind 
_This is an updated version of a project done in August 2019_


## The Problem
Finding a mental health care practitioner can be confusing and time consuming. With the current health care system in the United States, navigating an already complex system can make it difficult for patients to find the care they need. This problem can be escalated by the stigma that surrounds mental health. The <a href="https://www.apa.org/news/press/releases/2019/05/mental-health-survey">American Psychological Association</a> reported that while public opinion toward mental health is becoming more positive, there is still significant stigma associated with mental health care. 

>"A total of 87% of American adults agreed that having a mental health disorder is nothing to be ashamed of, and 86% said they believe that people with mental health disorders can get better, according to the poll.
...
Despite this welcome news, some stigma still persists. ... 39% said they would view someone differently if they knew that person had a mental health disorder." [[1]](#1)
>

I wanted to create a way for patients to find practitioners that were easily accessible and within their health insurance plan. With Recommind, users can input relevant information about themselves (ie. insurance provider, language, specialty, location, etc.) and will receive information on the top 5 best matches ordered by distance. 

## The Data
In August 2019, I used the <a href="https://betterdoctor.com/">BetterDoctor API</a> to retrieve information on practitioners in a hand-selected list of mental health specialties (67 total) within a 50 mile radius of Manhattan. 

The data included:
- Practice locations
- Insurances accepted
- Gender
- Languages spoken

## The model
To create the content-based recommendation engine, I utilized the cosine similarity/distance algorithm, which is typically used for natural language processing. However, I found that my data would be well-suited to this algorithm. 
The data that a user inputs is vectorized and compared to each vectorized practitioner. The top 5 practitioners with the smallest cosine distance are returned. 
     
<p align="center">
<img src="https://www.oreilly.com/library/view/statistics-for-machine/9781788295758/assets/2b4a7a82-ad4c-4b2a-b808-e423a334de6f.png"
     alt="Cosine Similarity - O'Reilly"
     style="float: left; margin-right: 10px;" />
</p>

## Next Steps
Ideally I would like to be able to include the ability for users to weigh the parameters based on their needs. For example, maybe a patient is more concerned with finding a very specific specialist than one that is close by or that is on their insurance plan. People's health and health care needs are personal and unique, and I hope to be able to cater to those needs with future optimization. 

## References
<a id="1">[1]</a> 
Survey: Americans Becoming More Open About Mental Health. (2019). American Psychological Association. https://www.apa.org/news/press/releases/apa-mental-health-report
