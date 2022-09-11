# Mini-project IV

### [Assignment](assignment.md)

## Project/Goals
The project was aimed at accurately predicting loan approval given a set of demographic information about applicants.

## Hypothesis
The statistics I thought most likely to be predictive including whether the applicant already had a credit history, as having already been approved for loans is a good indicator someone will be indicated for more loans. Additionally, income seemed important as higher incomes make it easier to pay back a loan.

## EDA 
The columns containing loan amounts and applicant (and coapplicant) income had many outliers in addition to not being normally distributed, so logarithmic transformations were necessary. Additionally, credit history had the most significant number of null values, but I thought its importance warranted continuing to use it regardless.

## Process
(fill in what you did during EDA, cleaning, feature engineering, modeling, deployment, testing)
### EDA started by looking looking at missing values and descriptive statistics. This quickly made it very clear that Income and Loan Amount information contained many outliers because of their standard deviations that were very large relative to their means.
### From here, it was time to handle missing values. There were several categorical variables, for which I sadly decided to drop rows that were missing them because attempting to decide on a placeholder for whether or not people were married seemed counterproductive. The numerical categories I replaced missing values in with means, and then took the logarithm of LoanAmount and TotalIncome, a new column made from combining Applicant and Coapplicant income.
### Now came running a basic logarithmic regression model, before running another logarithmic regression but this time as part of a Grid Search in order to find optiaml parameters. 
### Up next was setting up the entire previous process in a pipeline in order to make it harder to have errors creep into the data, and also to save on lines of code.
### From here, it was time to set up an API and deploy the API to AWS.

## Results/Demo
The model performed with an accuracy of 80%. The API takes information in JSON form before outputting a prediction on how likely the loan is to be rejected/approved.

## Challanges 
Challenges included setting up a pipeline, as combinging and taking the logs of columns directly within a pipeline proved difficult. Additionally, because I ended up keeping much of the column transformations separate from the pipeline, this then led to issues with the API because I had to manipulate the provided input into looking like the data after my column transformations, without being able to create dummies because only one row of data was being passed at a time.

## Future Goals
With more time I would have gotten more of the data manipulation inserted into the pipeline, instead of being a preliminary step that the API then handled manipulating into the right form. An issue of bias arises from the Gender variable: while the model is (slightly) more predictive when it is included, this indicates that the training data reflected some level of gender bias in loan applications. As such, I left it out of the final model.
