#-------------------------------------------------------------------------
# AUTHOR: Collaboration by Maribel G, Van H, Ken S., Kim M., Qinyi W.
#
# FILENAME: TeamProject_MVKKQ.py
#
# SPECIFICATION: This program reads in the file: diabetes_012_health_indicators.csv
#   removes the header line
#   removes any entries corresponding to anyone over the age of 12 : data_selection.csv
#   designates the first 1,000 entries as test data: data_to_TEST_with.csv
#   designates the rest of entries as training data: data_to_TRAIN_with.csv
#
# FOR: CS 4210 - Team Project
#
# TIME SPENT: Many hours discussing topic, goal, data source, who does what,
#-----------------------------------------------------------------------*/


#importing some Python libraries
from sklearn import tree
import matplotlib.pyplot as plt
import csv
db = []
X = []
Y = []

original_data_count = 0
data_selection_count = 0
data_processing_count = 0
data_transformed_count = 0

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##
## PHASE 1 OF 3: PREPROCESSING
print("* * * PHASE 1 OF 3 * * *")
##
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##

## STEP 1
## DATA SOURE: https://www.kaggle.com
## DATA FILE: https://www.kaggle.com/code/hainescity/diabetes-health-indicators-dataset-pt-br/input
## 

#open csv data file for reading
print("\tSTEP #1 - DATA: Obtain original dataset\n")
input_file = open( "diabetes_012_health_indicators_BRFSS2015.csv", "r" )

## STEP 2
## SELECTION
## 

#skip the first line in the data file because its the header information
skip_line = input_file.readline()

#open the file for writing
print("\tSTEP #2 - SELECTION: Only entries for those under the age of 13\n")
output_file_ds = open( "data_selection.csv", "w" )

for line in input_file:                      # go through rest of lines
     original_data_count += 1
     if float(line.split(',')[19]) < 13.0:   # if field #20(age) is < 13.0,
         data_selection_count += 1
         output_file_ds.write( line )        # save to  output, else skip it
input_file.close()
output_file_ds.close()

print("\t\t entries in original file: ", original_data_count)
print("\t\t entries selected for use: ", data_selection_count)
print("\t\t entries eliminated :      ", original_data_count - data_selection_count, "\n")

## STEP 3
## PROCESSING
## 
print("\tSTEP #3 - PROCESSING\n")

#open the file for reading
input_file_dp = open( "data_selection.csv", "r" )
data_TRAIN = open( "data_to_TRAIN_with.csv", "w" )
data_TEST = open( "data_to_TEST_with.csv", "w" )
counter = 0
while counter < 1000:
    line_of_input = input_file_dp.readline()
    data_TEST.write( line_of_input )
    counter += 1

data_TEST.close()

for line_of_input in input_file_dp:
    data_TRAIN.write( line_of_input )
data_TRAIN.close()
input_file_dp.close()

## STEP 4
## TRANSFORMATION
##
print("\tSTEP #4 - TRANSFORMATION\n")

x_TRAIN = []
y_TRAIN = []
data_TRAIN = open( "data_to_TRAIN_with.csv", "r" )
for line_of_input in data_TRAIN:
    # Remove \n and break on commas.
    temp_list = line_of_input.rstrip().split( ',' )
    # Append float version of classification
    y_TRAIN.append( float(temp_list.pop( 0 ) ) )
    # Convert strings to floats
    for index in range(len(temp_list)):
        temp_list.append( float( temp_list.pop(0) ) )
    # Append attributes.
    x_TRAIN.append( temp_list )

data_TRAIN.close()

x_TEST = []
y_TEST = []
data_TEST = open( "data_to_TEST_with.csv", "r" )
for line_of_input in data_TEST:
    # Remove \n and break on commas.
    temp_list = line_of_input.rstrip().split( ',' )
    # Append float version of classification
    y_TEST.append( float(temp_list.pop( 0 ) ) )
    # Convert strings to floats
    for index in range(len(temp_list)):
        temp_list.append( float( temp_list.pop(0) ) )
    # Append attributes.
    x_TEST.append( temp_list )

data_TEST.close()

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##
## PHASE 2 OF 3: MACHINE LEARNING
print("* * * PHASE 2 OF 3 * * *")
##
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##

## STEP 5
## MACHINE LEARNING
##
print("\tSTEP #5 - MACHINE LEARNING \n")

##### pick the depth of the tree #######
#### Note: full depth takes over 20 hours ####
#### Note: for Team Proeject, focus is on depth =< 4
#clf = tree.DecisionTreeClassifier(criterion = 'entropy') # Figure_1_FullDataFile.png = all 21 attribures used
clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth= 1) #Figure_Depth_1.png
#clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth= 2) #Figure_Depth_2.png
#clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth= 3) #Figure_Depth_3.png
#clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth= 4) #Figure_Depth_4.png
#clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth= 5) #Figure_Depth_5.png
#clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth= 10) #Figure_Depth_10.png
clf = clf.fit(x_TRAIN, y_TRAIN)

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##
## PHASE 3 OF 3: POSTPROCESSING
print("* * * PHASE 3 OF 3 * * *")

##
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
##

## STEP 6
## EVALUATION
## 
print("\tSTEP #6 - EVALUATION\n")

tree.plot_tree(clf, feature_names=['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 'HeartDisease',
                                   'PhysicalActivity', "Fruits", "Veggies", "HeavyAlcohol", "AnyHealthCare",
                                   "NoDrBcCost", "GeneralHealth", "MentalHealth", "PhysicalHealth",
                                   "DifficultyWalking", "Sex", "Age", "Education", "Income"],
               class_names=['No', 'Yes', 'No'], filled=True, rounded=True)

text_representation = tree.export_text(clf)
print(text_representation)
with open("decistion_tree_TEXT_depth_1.log", "w") as fout:
    fout.write(text_representation)

plt.show()
