# House price prediction using computer vision

1. **Problem statement**

    All people are supposed to have their own home and buying a home is an important step for a human being. Our house price needs to be affordable for the majority with decent income.
    
   In reality, in Ontario for example, less than half of the population can afford a down payment for a house. This is the problem because of the rapid increase of the price in Ontario when the income doesn’t increase at the same rate. So the problem of finding the best price for a  house related to our income and savings is critical in Ontario.
  
    To find a way to reduce that impact, I decided to answer those question:
      
      What can be the best estimated price of a house in Ontario based on the features of the house and image of the house to avoid overpricing by the seller?
      Which areas are the most profitable to acquire a new property?
    
    Unfortunately, access to Ontario house data was not public and will use datasets of Portland houses sold recently from redfin website  to build a model that will be able to give us the most accurate estimated price possible. Also, we will have a look of meaningful features that have direct or some kind of effect on house price.

2. **Data collection**

    For this problem, I decided to use the website redfin to scrape our tabular and image data of the houses. I first tried to scrape data on Zillow but the website was blocking the use of python code to scrape data on their website. I decided to use an alternative website called Redfin. To scrape data in redfin, I used python codes using selenium and beautiful soup libraries. This codes help me to scrape 239 house data(URL,sold price,#bedroom,#bathroom,#square feet,address,type of the house,year of construction, estimated price and price per sqft). I put all this data in a CSV file called “houses”. Also, with this code, I was able to scrape ~5000 images of the different 239 houses. After getting those images, I created another python code to put all the images on the same size and especially cropped them because some of them had white space. I put all the clean images in the folder called “cropped houses”. Also note that our tabular data had some missing value on 5 features and we used the median to replace those missing values.

3. **Data exploration and visualization**
![Features](https://github.com/laussin86/Housing-price-with-tabular-data-mixed-with-images/blob/main/description.png?raw=true)
    I   noticed here for example that the average price of a house sold is $586,873 while the average sold price based on redfin estimator is $580,618 so a difference of $6,255 on average. We can notice that the houses sold have on average 3 bedroom and 2 bathroom so give us an insight of the importance of bedroom and bathroom for people in Portland,OR or maybe people looking for a house are more family than singles or couples. We can notice as well that the average year of construction of those houses is 1957 with 75% of the houses built between 1956 and 1982 with the newest home sold in 2023. We can also note that the average sq ft is1,966 and the average price is $312.61. 

![Correlation](https://github.com/laussin86/Housing-price-with-tabular-data-mixed-with-images/blob/main/correlation.png?raw=true)
    
![most house sold](https://github.com/laussin86/Housing-price-with-tabular-data-mixed-with-images/blob/main/house%20sold.png?raw=true)

most of the houses sold are single family residential. This confirmed my assumption stated  earlier that people buying the houses were more family.


4. **Data preprocessing**

    In this section, I started first to  check the unique values of each categorical value and  dropped the categorical features that have too many unique values. So we drop the URL and address.
    
     city and zip code has positive correlation was confirm by the chi-square test :
     
     Chi-square statistic: 1248.0
     
     p-value: 2.606664370697648e-149
     
     The extremely low p-value indicates that the probability of observing such a large Chi-square statistic under the null hypothesis of no association is very low, so you can reject the null hypothesis and conclude that there is a significant relationship between the two variables.But we will keep both as there are no influence in the models. 
     
     The last features dropped are the estimated price has a correlation of 1 with price as  we will use those estimated prices to see if our model can beat or be close to the estimation system of redfin and price per sqft as i realized that it increased bias.
     
     The next step was to use the one-hot encoding to encode our categorical features. 
     
     Finally, we have split our data to 80% train and 20% test and also normalize them. 

    
5. **Model selection and training**

    For my baseline model selection, I chose the  xgboost regressor as my baseline model to improve on. So I started  by using GridSearchCV() to search for the best model parameters in a parameter space provided by me.
   
   then train our model based on those best parameters and then predict the mean absolute error(MAE). 
   
   Our baseline MAE is XGBoost MAE = 86524.93563988095  or XGBoost MAPE = 16.836234478793596 that shows the percentage.
   
   I chose the mean absolute error (MAE) as our performance metric to evaluate and compare models. MAE presents a value that is easy to understand; it shows the average value of model error. 
   
   We noticed as well that the mean is 589,289 and the median is 530,000. We can see also that the first quartile is 414,750; this means that 75% of the data is larger than this number.Now looking at XGBoost error of 38,176.31, we can say that an error of about 38,000 is okay but still large for us for data whose mean is 589,289 and whose 75% of it is larger than 414,750. But will try to improve by constructing a neural network using the image house and those text data.
   
   ![Feature importance](https://github.com/laussin86/Housing-price-with-tabular-data-mixed-with-images/blob/main/Features%20importance.png?raw=true)
   
   Finally, We Noticed that City_portland 97221 ,City_portland 97219, bath, Sqft respectively were the most important features to predict the house price.


6. **Improved Model based on the baseline model**

    Our reflection to improve our MAE or MAPE was to use the image of the houses concatenated with the tabular data using a neural network to see if it will improve our model.
    
    ![Architecture](https://github.com/laussin86/Housing-price-with-tabular-data-mixed-with-images/blob/main/architecture.png?raw=true)
    
   

7. **Comparing result**

     I focused my mixed data neural network in 2 models. The first one was putting images per house and predicting the price based on the images and the text data. For that model, we got result as:
     


	| **Models** | **MAPE** |
	| ------------ | ------------ | 
	| *XGboost Regressor* | *16.84%* |
	| *Mix data* | *11.88%* | 
	| *Mix data with categorized images* | *8.55%* | 


  
