# House price prediction using computer vision

1. **Problem statement**

    All people are supposed to have their own home and buying a home is an important step for a human being. Our house price needs to be affordable for the majority with decent income.
    
   In reality, in Ontario for example, less than half of the population can afford a down payment for a house. This is the problem because of the rapid increase of the price in Ontario when the income doesn’t increase at the same rate. So the problem of finding the best price for a  house related to our income and savings is critical in Ontario.

    In consequence, some data found that 57 per cent of people  believed they won’t ever afford a home, while more than half (54 per cent) of parents in Ontario do not plan on helping their children buy a home soon. Also 80 per cent of current Ontario homeowners are not planning to sell their homes in the next two-to-three years, compared to 77 per cent in 2021.
  
    To find a way to reduce that impact, I decided to answer those question:
      
      What can be the best estimated price of a house in Ontario based on the features of the house and image of the house to avoid overpricing by the seller?
      Which areas are the most profitable to acquire a new property?
    
    Unfortunately, access to Ontario house data was not public and will use datasets of Portland houses sold recently from redfin website  to build a model that will be able to give us the most accurate estimated price possible. Also, we will have a look of meaningful features that have direct or some kind of effect on house price.

2. **Data collection**

    For this problem, I decided to use the website redfin to scrape our tabular and image data of the houses. I first tried to scrape data on Zillow but the website was blocking the use of python code to scrape data on their website. I decided to use an alternative website called Redfin. To scrape data in redfin, I used python codes using selenium and beautiful soup libraries. This codes help me to scrape 239 house data(URL,sold price,#bedroom,#bathroom,#square feet,address,type of the house,year of construction, estimated price and price per sqft). I put all this data in a CSV file called “houses”. Also, with this code, I was able to scrape ~5000 images of the different 239 houses. After getting those images, I created another python code to put all the images on the same size and especially cropped them because some of them had white space. I put all the clean images in the folder called “cropped houses”. Also note that our tabular data had some missing value on 5 features and we used the median to replace those missing values.

3. **Data exploration and visualization**

    I started first to check the datatype of our tabular dataset houses. I found out that we have 11 features for 239 houses but I decided to use 208 houses because I had images for only 208 houses due to the fact that redfin blocked images for some houses. The types of features are 5 floats, 3 integers and 4 objects or categorical types.

    I   noticed here for example that the average price of a house sold is $586,873 while the average sold price based on redfin estimator is $580,618 so a difference of $6,255 on average. We can notice that the houses sold have on average 3 bedroom and 2 bathroom so give us an insight of the importance of bedroom and bathroom for people in Portland,OR or maybe people looking for a house are more family than singles or couples. We can notice as well that the average year of construction of those houses is 1957 with 75% of the houses built between 1956 and 1982 with the newest home sold in 2023. We can also note that the average sq ft is1,966 and the average price is $312.61. 

    The next steps was to check the correlation between the features and the target variable.notice the features with strongest correlation with sold price with exception of estimated price are first sqft followed by number of bathrooms with correlation more than 0.5. The 2 next features with positive correlation with sold price are # bedroom and price per sqft. We can note for example that year_built and Zip code have low(positive and negative) or no correlation with the sold price. It can be explained by the fact people are looking more for space, number room , and how well maintained the house is. 
    
    One last thing I want to notice is hat most of the houses sold are single family residential. This confirmed my assumption stated  earlier that people buying the houses were more family. And also, the majority of the houses are located in the zip code area between 97200 and 97250.
    
    all those comment can be visualize inside the project outline or the code.

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
The parameter "max_depth" sets the maximum depth of a tree,


   - "learning_rate" represents the step size shrinkage used in updating weights,


   - "n_estimators" specifies the number of boosted trees to fit,


   - "booster" determines which booster to use,


   - "gamma" specifies the minimum loss reduction required to make a further partition on a leaf node of the tree,


   - "subsample" is subsample ratio of the training instances; this subsampling will occur once in every boosting iteration,


   - "colsample_bytree" specifies the subsample ratio of columns when constructing each tree,


   - "colsample_bylevel" specifies the subsample ratio of columns for each split, in each level,


   - "reg_alpha" is L1 regularization term, and


   - "reg_lambda" is L2 regularization term
  
   The gridsearch gave us those result below with cv=5 for our XGboost regressor:
   
   Best parameters:
   
    {'subsample': 0.3, 'reg_lambda': 3, 'reg_alpha': 33, 'n_estimators': 700, 'max_depth': 5, 'learning_rate': 0.009, 'gamma': 7, 'colsample_bytree': 0.7, 'colsample_bylevel': 0.5, 'booster': 'gbtree'}
   
   then train our model based on those best parameters and then predict the mean absolute error(MAE). 
   
   Our baseline MAE is XGBoost MAE = 86524.93563988095  or XGBoost MAPE = 16.836234478793596 that shows the percentage.
   
   I chose the mean absolute error (MAE) as our performance metric to evaluate and compare models. MAE presents a value that is easy to understand; it shows the average value of model error. For example, for our XGBoost model, its MAE is 86,524.93 which means that on average, XGBoost will predict a value that is bigger or smaller than the true value by 86,524.93. Now to understand how good this MAE is, we need to know the range and distribution of the data. In our case, we need to see the values of the target variable price which contains the actual house prices.
   
   We noticed as well that the mean is 589,289 and the median is 530,000. We can see also that the first quartile is 414,750; this means that 75% of the data is larger than this number.Now looking at XGBoost error of 38,176.31, we can say that an error of about 38,000 is okay but still large for us for data whose mean is 589,289 and whose 75% of it is larger than 414,750. But will try to improve by constructing a neural network using the image house and those text data.
   
   Finally, We Noticed that City_portland 97221 ,City_portland 97219, bath, Sqft respectively were the most important features to predict the house price.


6. **Improved Model based on the baseline model**

    Our reflection to improve our MAE or MAPE was to use the image of the houses concatenated with the tabular data using a neural network to see if it will improve our model.
    
    To do that architecture, I will need to create each branch at the time.
    
    1. I started with the text data so the numerical and categorical data first.I inputed our numerical and categorical data. Then,I created the function process_house_attributes to normalize our tabular data.
    2. Next step will be to process the image data. For that, I created the load_house_images function that has a function to input the image and group each image by house.
    3. After, I created our MLP(Multi-layer Perceptron) function  to process our tabular data but not to get the regression result, just to be a branch like the figure below.in the same way, I created a CNN network to process our images.
    4. Mix trained our data.
    5. Concatenated the 2 models(CNN and MLP)
    6. Finally,created the final FC layers with the last one having a linear activation.
    7. Predict and analyze the result.
    
   

7. **Comparing result**

     I focused my mixed data neural network in 2 models. The first one was putting images per house and predicting the price based on the images and the text data. For that model, we got result as:
     
    avg. house price: $586,873.29, std house price: $356,533.20
    
    MAPE: 11.88%, std: 8.65%

    The second model we did the same thing but isolating image per category(bedroom, bathroom,living room and front view) and we got the result as:
    
    avg. house price: $586,873.29, std house price: $356,533.20
    
    MAPE: 8.55%, std: 6.64%

	


  
