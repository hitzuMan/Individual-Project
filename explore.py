import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import opendatasets as od
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb








# Function to split the data into training, validation, and test sets, and create a majority class baseline model
def split_data_and_create_baseline(X, Y, random_state=42):
    # Split the data into training (70%), validation (15%), and test (15%) sets
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.3, random_state=random_state)
    X_validation, X_test, Y_validation, Y_test = train_test_split(X_val, Y_val, test_size=0.5, random_state=random_state)

    # Scale the data using StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_validation = sc.transform(X_validation)
    X_test = sc.transform(X_test)

    # Create a majority class baseline model
    majority_class_baseline = DummyClassifier(strategy="most_frequent")
    majority_class_baseline.fit(X_train, Y_train)
    predictions = majority_class_baseline.predict(X_test)
    accuracy = accuracy_score(Y_test, predictions)
    
    return X_train, Y_train, X_validation, Y_validation, X_test, Y_test, accuracy






# Call the function and provide the DataFrame and other arguments
# P values for the correlation test is below .05
def calculate_t_test(df, selected_features, target_variable, significance_level=0.05):
    t_test_results = []
    for feature in selected_features:
        group_0 = df[df[target_variable] == 0][feature]
        group_1 = df[df[target_variable] == 1][feature]

        t_stat, p_value = stats.ttest_ind(group_0, group_1)
        t_test_results.append((feature, t_stat, p_value))

    print("T-Test Results:")
    for feature, t_stat, p_value in t_test_results:
        print(f'T-Test between {feature} and {target_variable}:')
        print(f'T-Statistic: {t_stat:.4f}')
        print(f'P-value: {p_value:.4f}')
        print('')

        if p_value < significance_level:
            print(f'T-Test between {feature} and {target_variable} is statistically significant.')
        else:
            print(f'T-Test between {feature} and {target_variable} is not statistically significant.')

# Example usage:
# Assuming df is your DataFrame, selected_features is your list of features, and target_variable is the target variable.
#calculate_t_test(df, selected_features, target_variable)







# Function to perform univariate analysis
def univariate_analysis(df):
    # Univariate analysis of 'concave points_mean'
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 3, 1)
    sns.histplot(df['concave points_mean'], kde=True)
    plt.title('Distribution of concave points_mean')

    # Univariate analysis of 'radius_worst'
    plt.subplot(1, 3, 2)
    sns.histplot(df['radius_worst'], kde=True)
    plt.title('Distribution of radius_worst')

    # Univariate analysis of 'perimeter_worst'
    plt.subplot(1, 3, 3)
    sns.histplot(df['perimeter_worst'], kde=True)
    plt.title('Distribution of perimeter_worst')

    # Univariate analysis of 'concave points_mean'
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 3, 1)
    sns.histplot(df['concave points_worst'], kde=True)
    plt.title('Distribution of concave points_worst')

    plt.tight_layout()
    plt.show()

    
# Function to perform bivariate analysis
def bivariate_analysis(df):
    features = ['concave points_mean', 'radius_worst', 'perimeter_worst', 'concave points_worst']
    titles = ['Bivariate Analysis: concave points_mean vs. Diagnosis',
              'Bivariate Analysis: radius_worst vs. Diagnosis',
              'Bivariate Analysis: perimeter_worst vs. Diagnosis',
              'Bivariate Analysis: concave points_worst vs. Diagnosis']

    plt.figure(figsize=(16, 12))

    for i, feature in enumerate(features):
        plt.subplot(2, 2, i + 1)
        sns.boxplot(data=df, x='diagnosis', y=feature)
        plt.title(titles[i])

        medians = df.groupby('diagnosis')[feature].median()
        for j, median in enumerate(medians):
            plt.text(j, median, f'Median: {median:.2f}', horizontalalignment='center', verticalalignment='bottom', fontsize=10, color='white')

    plt.tight_layout()
    plt.show()
    
    
    
    
# Function to perform multivariate analysis
def multivariate(df):
    # Create a DataFrame with the selected features and diagnosis
    selected_features = ['concave points_mean', 'concave points_worst', 'perimeter_worst', 'radius_worst']
    df_selected = df[selected_features + ['diagnosis']]

    # Define color mapping for diagnosis
    color_mapping = {0: 'blue', 1: 'orange'}

    # Create the 3D scatter plot with color mapping
    fig = px.scatter_3d(df_selected, x='concave points_mean', y='concave points_worst', z='perimeter_worst',
                        color='diagnosis', symbol='diagnosis', opacity=0.7,
                        color_discrete_map=color_mapping,
                        labels={'concave points_mean': 'Concave Points Mean',
                                'concave points_worst': 'Concave Points Worst',
                                'perimeter_worst': 'Perimeter Worst',
                                'radius_worst': 'Radius Worst'},
                        title='3D Cluster Plot of Selected Features by Diagnosis')

    # Customize the layout
    fig.update_layout(legend_title_text='Diagnosis')
    fig.update_traces(marker=dict(size=4))

    # Show the interactive plot
    fig.show()
    
    
  
    
    
    
    
    
    
    
    
    
