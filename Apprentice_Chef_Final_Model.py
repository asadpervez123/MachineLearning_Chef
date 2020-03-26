#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Name : Mohammad Asad Pervez
# Email       : asadpervez@hotmail.com
# Phone        : 8572614055

################################################################################
# Import Packages
################################################################################


# importing packages
import pandas as pd # data science essentials
from sklearn.model_selection import train_test_split # train/test split
import sklearn.linear_model #for linear models
from sklearn.tree import DecisionTreeRegressor #Decision Tree Regressor Model


# In[ ]:


################################################################################
# Load Data
################################################################################

# use this space to load the original dataset
# MAKE SURE TO SAVE THE ORIGINAL FILE AS original_df
# Example: original_df = pd.read_excel('Apprentice Chef Dataset.xlsx')


original_df     = pd.read_excel('Apprentice_Chef_Dataset.xlsx')


# In[ ]:


################################################################################
# Feature Engineering, Variable Selection and (optional) Dataset Standardization
################################################################################

# use this space for all of the feature engineering that is required for your

#splitting emails

email_list = []

for index, col in original_df.iterrows():
    
    # splitting email domain at '@'
    split_email = original_df.loc[index, 'EMAIL'].split(sep = '@')
    
    # appending placeholder_lst with the results
    email_list.append(split_email)
    

# converting placeholder_lst into a DataFrame 
domains = pd.DataFrame(email_list)

domains.columns = ['email_name', 'personal_email_domain']

# concatenating personal_email_domain with friends DataFrame
original_df = pd.concat([original_df, domains.loc[: , 'personal_email_domain']],
                   axis = 1)

#making lists of email groups

professional_email_domains = ['@mmm.com',
                                '@amex.com',
                                '@apple.com',
                                '@boeing.com',
                                '@caterpillar.com',
                                '@chevron.com',
                                '@cisco.com',
                                '@cocacola.com',
                                '@disney.com',
                                '@dupont.com',
                                '@exxon.com',
                                '@ge.org',
                                '@goldmansacs.com',
                                '@homedepot.com',
                                '@ibm.com',
                                '@intel.com',
                                '@jnj.com',
                                '@jpmorgan.com',
                                '@mcdonalds.com',
                                '@merck.com',
                                '@microsoft.com',
                                '@nike.com',
                                '@pfizer.com',
                                '@pg.com',
                                '@travelers.com',
                                '@unitedtech.com',
                                '@unitedhealth.com',
                                '@verizon.com',
                                '@visa.com',
                                '@walmart.com']

personal_email_domains = ['@gmail.com',
                            '@yahoo.com',
                            '@protonmail.com']

junk_email_domains = ['@me.com',
                        '@aol.com',
                        '@hotmail.com',
                        '@live.com',
                        '@msn.com',
                        '@passport.com']

#grouping_emails
email_groups = []

for i in original_df.loc[ : , 'personal_email_domain']:
    if '@' + i in professional_email_domains:
        email_groups.append('professional')
    
    elif '@' + i in personal_email_domains:
        email_groups.append ('personal')
    
    elif '@' + i in junk_email_domains:
        email_groups.append ('junk')
    
    else:
        email_groups.append('unknown')
        
original_df['email_groups'] = pd.Series(email_groups)

#Saving New Dataset to Excel
original_df.to_excel('Apprentice_ND.xlsx')

#importing the file as chef
chef = pd.read_excel('Apprentice_ND.xlsx')


# setting outlier thresholds

REVENUE_split = 2400 
TOTAL_MEALS_ORDERED_split =200
UNIQUE_MEALS_PURCH_split = 10.0
CONTACTS_W_CUSTOMER_SERVICE_split = 10.0
AVG_TIME_PER_SITE_VISIT_split = 200
CANCELLATIONS_BEFORE_NOON_split = 5
CANCELLATIONS_AFTER_NOON_split_low = 0.5
CANCELLATIONS_AFTER_NOON_split_high = 1.5
MOBILE_LOGINS_split_low = 4.9
MOBILE_LOGINS_split_high = 6.1
PC_LOGINS_split_low = 0.5
PC_LOGINS_split_high = 2.4
WEEKLY_PLAN_split_low = 0
WEEKLY_PLAN_split_high = 17
EARLY_DELIVERIES_split = 1
LATE_DELIVERIES_split = 10
PACKAGE_LOCKER_split_low = 0.0
PACKAGE_LOCKER_split_high = 1.0
AVG_PREP_VID_TIME_split = 250
LARGEST_ORDER_SIZE_split_low = 2 
LARGEST_ORDER_SIZE_split_high = 7
MASTER_CLASSES_ATTENDED_split = 2
MEDIAN_MEAL_RATING_split = 4
AVG_CLICKS_PER_VISIT_split_low = 8
TOTAL_PHOTOS_VIEWED_split_low = 0
TOTAL_PHOTOS_VIEWED_split_high = 400


##############################################################################
## Feature Engineering (outlier thresholds)                                 ##
##############################################################################

# developing features (columns) for outliers

#Revenue
chef['out_revenue'] = 0

revenue_condition_split = chef.loc[: , 'out_revenue'][chef['REVENUE']>REVENUE_split]
chef['out_revenue'].replace(to_replace = revenue_condition_split,
                            value = 1,
                           inplace = True)

#Total meals ordered
chef['out_meals_ordered'] = 0

total_meals_ordered_hi_split = chef.loc[: ,'out_meals_ordered'][chef['TOTAL_MEALS_ORDERED'] > TOTAL_MEALS_ORDERED_split]
chef['out_meals_ordered'].replace(to_replace = total_meals_ordered_hi_split,
                                   value = 1,
                                    inplace = True)

#Unique Meals
chef['out_unique_meals'] = 0

unique_meals_condition = chef.loc[: , 'out_unique_meals'][chef['UNIQUE_MEALS_PURCH'] >= UNIQUE_MEALS_PURCH_split]
chef['out_unique_meals'].replace(to_replace = unique_meals_condition,
                                value = 1,
                                inplace = True)

#Contact with Customer Service
chef['out_customer_service_contact'] = 0

customer_service_contact_condition = chef.loc[: , 'out_customer_service_contact'][chef['CONTACTS_W_CUSTOMER_SERVICE'] > CONTACTS_W_CUSTOMER_SERVICE_split]

chef['out_customer_service_contact'].replace(to_replace = customer_service_contact_condition,
                                value = 1,
                                inplace = True)

#Avg time on site
AVG_TIME_PER_SITE_VISIT_split = 200

chef['out_avg_time_site_visit'] = 0
avg_time_condition_split = chef.loc[: , 'out_avg_time_site_visit'][chef['AVG_TIME_PER_SITE_VISIT']>AVG_TIME_PER_SITE_VISIT_split]
chef['out_avg_time_site_visit'].replace(to_replace = avg_time_condition_split,
                            value = 1,
                           inplace = True)


#cancellations before noon
CANCELLATIONS_BEFORE_NOON_split = 5

chef['out_canc_before_noon'] = 0

out_canc_condition_split = chef.loc[: , 'out_canc_before_noon'][chef['CANCELLATIONS_BEFORE_NOON']>CANCELLATIONS_BEFORE_NOON_split]
chef['out_canc_before_noon'].replace(to_replace = out_canc_condition_split,
                            value = 1,
                           inplace = True)

#cancellation after noon
CANCELLATIONS_AFTER_NOON_split_low = 0.5
CANCELLATIONS_AFTER_NOON_split_high = 1.5

chef['out_CANCELLATIONS_AFTER_NOON'] = 0
condition_hi = chef.loc[0:,'out_CANCELLATIONS_AFTER_NOON'][chef['CANCELLATIONS_AFTER_NOON'] > CANCELLATIONS_AFTER_NOON_split_high]
condition_lo = chef.loc[0:,'out_CANCELLATIONS_AFTER_NOON'][chef['CANCELLATIONS_AFTER_NOON'] < CANCELLATIONS_AFTER_NOON_split_low]

chef['out_CANCELLATIONS_AFTER_NOON'].replace(to_replace = condition_hi,
                                    value      = 1,
                                    inplace    = True)

chef['out_CANCELLATIONS_AFTER_NOON'].replace(to_replace = condition_lo,
                                    value      = 1,
                                    inplace    = True)



#mobile logins
MOBILE_LOGINS_split_low = 4.9
MOBILE_LOGINS_split_high = 6.1

chef['out_MOBILE_LOGINS'] = 0
condition_hi = chef.loc[0:,'out_MOBILE_LOGINS'][chef['MOBILE_LOGINS'] > MOBILE_LOGINS_split_high]
condition_lo = chef.loc[0:,'out_MOBILE_LOGINS'][chef['MOBILE_LOGINS'] < MOBILE_LOGINS_split_low]

chef['out_MOBILE_LOGINS'].replace(to_replace = condition_hi,
                                    value      = 1,
                                    inplace    = True)

chef['out_MOBILE_LOGINS'].replace(to_replace = condition_lo,
                                    value      = 1,
                                    inplace    = True)

#PC logins
PC_LOGINS_split_low = 0.5
PC_LOGINS_split_high = 2.4

chef['out_PC_LOGINS'] = 0
condition_hi = chef.loc[0:,'out_PC_LOGINS'][chef['PC_LOGINS'] > PC_LOGINS_split_high]
condition_lo = chef.loc[0:,'out_PC_LOGINS'][chef['PC_LOGINS'] < PC_LOGINS_split_low]

chef['out_PC_LOGINS'].replace(to_replace = condition_hi,
                                    value      = 1,
                                    inplace    = True)

chef['out_PC_LOGINS'].replace(to_replace = condition_lo,
                                    value      = 1,
                                    inplace    = True)

#weekly plasn
WEEKLY_PLAN_split_low = 0
WEEKLY_PLAN_split_high = 17

chef['out_WEEKLY_PLAN'] = 0
condition_hi = chef.loc[0:,'out_WEEKLY_PLAN'][chef['WEEKLY_PLAN'] > WEEKLY_PLAN_split_high]
condition_lo = chef.loc[0:,'out_WEEKLY_PLAN'][chef['WEEKLY_PLAN'] == WEEKLY_PLAN_split_low]

chef['out_WEEKLY_PLAN'].replace(to_replace = condition_hi,
                                    value      = 1,
                                    inplace    = True)

chef['out_WEEKLY_PLAN'].replace(to_replace = condition_lo,
                                    value      = 1,
                                    inplace    = True)

#early deliveries
EARLY_DELIVERIES_split = 1
chef['out_EARLY_DELIVERIES'] = 0

EARLY_DELIVERIES_split_condition_split = chef.loc[: , 'out_EARLY_DELIVERIES'][chef['EARLY_DELIVERIES']<EARLY_DELIVERIES_split]
chef['out_EARLY_DELIVERIES'].replace(to_replace = EARLY_DELIVERIES_split_condition_split,
                            value = 1,
                           inplace = True)

#late deliveries
LATE_DELIVERIES_split = 10
chef['out_LATE_DELIVERIES'] = 0

LATE_DELIVERIES_condition_split = chef.loc[: , 'out_LATE_DELIVERIES'][chef['LATE_DELIVERIES']>LATE_DELIVERIES_split]
chef['out_LATE_DELIVERIES'].replace(to_replace = LATE_DELIVERIES_condition_split,
                            value = 1,
                           inplace = True)

#package locker
PACKAGE_LOCKER_split_low = 0.0
PACKAGE_LOCKER_split_high = 1.0

chef['out_PACKAGE_LOCKER'] = 0
condition_hi = chef.loc[0:,'out_PACKAGE_LOCKER'][chef['PACKAGE_LOCKER'] > PACKAGE_LOCKER_split_high]
condition_lo = chef.loc[0:,'out_PACKAGE_LOCKER'][chef['PACKAGE_LOCKER'] < PACKAGE_LOCKER_split_low]

chef['out_PACKAGE_LOCKER'].replace(to_replace = condition_hi,
                                    value      = 1,
                                    inplace    = True)

chef['out_PACKAGE_LOCKER'].replace(to_replace = condition_lo,
                                    value      = 1,
                                    inplace    = True)


#average video time
AVG_PREP_VID_TIME_split = 250
chef['out_AVG_PREP_VID_TIME'] = 0

AVG_PREP_VID_TIME_condition_split = chef.loc[: , 'out_AVG_PREP_VID_TIME'][chef['AVG_PREP_VID_TIME']>AVG_PREP_VID_TIME_split]
chef['out_AVG_PREP_VID_TIME'].replace(to_replace = AVG_PREP_VID_TIME_condition_split,
                            value = 1,
                           inplace = True)

#largest orrder size
LARGEST_ORDER_SIZE_split_low = 2 
LARGEST_ORDER_SIZE_split_high = 7

chef['out_LARGEST_ORDER_SIZE'] = 0
condition_hi = chef.loc[0:,'out_LARGEST_ORDER_SIZE'][chef['LARGEST_ORDER_SIZE'] > LARGEST_ORDER_SIZE_split_high]
condition_lo = chef.loc[0:,'out_LARGEST_ORDER_SIZE'][chef['LARGEST_ORDER_SIZE'] < LARGEST_ORDER_SIZE_split_low]

chef['out_LARGEST_ORDER_SIZE'].replace(to_replace = condition_hi,
                                    value      = 1,
                                    inplace    = True)

chef['out_LARGEST_ORDER_SIZE'].replace(to_replace = condition_lo,
                                    value      = 1,
                                    inplace    = True)

#master classes attended
MASTER_CLASSES_ATTENDED_split = 2
chef['out_MASTER_CLASSES_ATTENDED'] = 0

MASTER_CLASSES_ATTENDED_condition_split = chef.loc[: , 'out_MASTER_CLASSES_ATTENDED'][chef['MASTER_CLASSES_ATTENDED']>MASTER_CLASSES_ATTENDED_split]
chef['out_MASTER_CLASSES_ATTENDED'].replace(to_replace = revenue_condition_split,
                            value = 1,
                           inplace = True)

#median meal rating
MEDIAN_MEAL_RATING_split = 4
chef['out_MEDIAN_MEAL_RATING'] = 0

MEDIAN_MEAL_RATING_condition_split = chef.loc[: , 'out_MEDIAN_MEAL_RATING'][chef['MEDIAN_MEAL_RATING']>MEDIAN_MEAL_RATING_split]
chef['out_MEDIAN_MEAL_RATING'].replace(to_replace = MEDIAN_MEAL_RATING_condition_split,
                            value = 1,
                           inplace = True)

#average clicks per visit
AVG_CLICKS_PER_VISIT_split_low = 8
chef['out_AVG_CLICKS_PER_VISIT'] = 0

AVG_CLICKS_PER_VISIT_condition_split = chef.loc[: , 'out_AVG_CLICKS_PER_VISIT'][chef['AVG_CLICKS_PER_VISIT']<AVG_CLICKS_PER_VISIT_split_low]
chef['out_AVG_CLICKS_PER_VISIT'].replace(to_replace = AVG_CLICKS_PER_VISIT_condition_split,
                            value = 1,
                           inplace = True)

#total photos viewed
TOTAL_PHOTOS_VIEWED_split_low = 0
TOTAL_PHOTOS_VIEWED_split_high = 400

chef['out_TOTAL_PHOTOS_VIEWED'] = 0
condition_hi = chef.loc[0:,'out_TOTAL_PHOTOS_VIEWED'][chef['TOTAL_PHOTOS_VIEWED'] > TOTAL_PHOTOS_VIEWED_split_high]
condition_lo = chef.loc[0:,'out_TOTAL_PHOTOS_VIEWED'][chef['TOTAL_PHOTOS_VIEWED'] == TOTAL_PHOTOS_VIEWED_split_low]

chef['out_TOTAL_PHOTOS_VIEWED'].replace(to_replace = condition_hi,
                                    value      = 1,
                                    inplace    = True)

chef['out_TOTAL_PHOTOS_VIEWED'].replace(to_replace = condition_lo,
                                    value      = 1,
                                    inplace    = True)


#Total Meals Ordered Scatter
TOTAL_MEALS_ORDERED_scat_out = 300

chef['TOTAL_MEALS_ORDERED_scat_out'] = 0
TOTAL_MEALS_ORDERED_scat_condition_split = chef.loc[: , 'TOTAL_MEALS_ORDERED_scat_out'][chef['TOTAL_MEALS_ORDERED']>=TOTAL_MEALS_ORDERED_scat_out]
chef['TOTAL_MEALS_ORDERED_scat_out'].replace(to_replace = TOTAL_MEALS_ORDERED_scat_condition_split,
                            value = 1,
                           inplace = True)




#Latgest Order Size
LARGEST_ORDER_SIZE_scat_out = 10
chef['LARGEST_ORDER_SIZE_scat_out'] = 0

LARGEST_ORDER_SIZE_scat_out_scat_condition_split = chef.loc[: , 'LARGEST_ORDER_SIZE_scat_out'][chef['LARGEST_ORDER_SIZE']>=LARGEST_ORDER_SIZE_scat_out]
chef['LARGEST_ORDER_SIZE_scat_out'].replace(to_replace = LARGEST_ORDER_SIZE_scat_out_scat_condition_split,
                            value = 1,
                           inplace = True)



#marking outliers for the email group
email_group_out = 6000

chef['out_email_group'] = 0

out_email_group_condition_split = chef.loc[: , 'out_email_group'][chef['REVENUE']>email_group_out]
chef['out_email_group'].replace(to_replace = out_email_group_condition_split,
                            value = 1,
                           inplace = True)

chef.to_excel('chef_feature_rich.xlsx', index=False)


# one hot encoding categorical variables
one_hot_email  = pd.get_dummies(chef['email_groups'])



# final model


# declaring set of x-variables
x_variables = ['TOTAL_MEALS_ORDERED', 'UNIQUE_MEALS_PURCH', 'CONTACTS_W_CUSTOMER_SERVICE', 
             'CANCELLATIONS_BEFORE_NOON', 'MOBILE_LOGINS', 
             'AVG_PREP_VID_TIME', 'LARGEST_ORDER_SIZE', 'MASTER_CLASSES_ATTENDED', 'MEDIAN_MEAL_RATING', 
             'out_unique_meals', 'out_customer_service_contact', 'out_canc_before_noon', 
             'out_CANCELLATIONS_AFTER_NOON', 'out_WEEKLY_PLAN', 'out_AVG_PREP_VID_TIME','out_MASTER_CLASSES_ATTENDED', 
             'out_MEDIAN_MEAL_RATING', 'out_email_group']



original_df = chef.copy()
# Preparing a DataFrame based the the analysis above
explanatory_data = original_df.loc[ : , x_variables]


# Preparing the target variable
target_data      = original_df.loc[ : , 'REVENUE']


# In[ ]:


################################################################################
# Train/Test Split
################################################################################

# this is the exact code we were using before
X_train, X_test, y_train, y_test = train_test_split(
            explanatory_data,
            target_data,
            test_size = 0.25,
            random_state = 222)


# In[ ]:


################################################################################
# Final Model (instantiate, fit, and predict)
################################################################################

# use this space to instantiate, fit, and predict on your final model

# INSTANTIATING a model object
tree_model = sklearn.tree.DecisionTreeRegressor(max_depth=6, random_state=222)


# FITTING the training data
tree_fit = tree_model.fit(X_train, y_train)


# PREDICTING on new data
tree_pred = tree_fit.predict(X_test)


print('Training Score:', tree_model.score(X_train, y_train).round(3))
print('Testing Score:',  tree_model.score(X_test, y_test).round(3))

# In[ ]:


################################################################################
# Final Model Score (score)
################################################################################

test_score = tree_model.score(X_test, y_test).round(3)

