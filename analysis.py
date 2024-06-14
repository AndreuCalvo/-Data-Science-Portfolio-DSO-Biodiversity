import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

observations_data = pd.read_csv('observations.csv')
### EDA OBSERVATIONS ###
#print(observations_data.info())
#print(observations_data.head())

### scientific_name feature ###
#print(observations_data.scientific_name.unique)
#print(observations_data.scientific_name.value_counts())
#the scientific_name have a unique value per row/observation, the type is a string and define the name of the animal

### park_name feature ###
#print(observations_data.park_name.value_counts())
#the park_name is a nominal categorical variable, exist 4 types of park_name: Great Smoky Mountains National Park, Yosemite National Park, Bryce National Park and Yellowstone National Park, any of theme have 5824 observations. This variable define the park where owns the animal observed

### observations feature ###
#print(observations_data.observations.describe())
# the observations is a int variable, exist 23296 observations, any of them are null. This variable define de number of observations of the animal. The mean is 142 observations per animal and the std is 69. The min value is 9 and the max value is 321 
#plt.hist(observations_data.observations)
#plt.title('histogram observations feature')
#plt.xlabel('obsevations')
#plt.ylabel('number observations')
#plt.savefig('histogram_observations_feature.png')
#plt.show()
#plt.clf()
# the hist plot doesn't have a normal distribution. It has two peaks

### EDA SPECIES INFO ###
species_info_data = pd.read_csv('species_info.csv')
#print(species_info_data.head())
#print(species_info_data.info())
# this dataset has a 5824 observations with 4 features: category, scientific_name, common_names and conservation_status

### category feature ###
#print(species_info_data.category.unique())
#print(species_info_data.category.value_counts())
# the category is a nominal categorical variable with 7 categories: Vascular Plant - 4470, Bird - 521, Nonvascular Plant - 333, Mammal - 214, Fish - 127,  Amphibian - 80 and Reptile - 79

### scientific_name feature###
#print(species_info_data.scientific_name.unique)
#the scientific_name have a unique value per row/observation, the type is a string and define the name of the animal. This feature link the two datasets, species info and observations

### common names feature ###
#print(species_info_data.common_names.value_counts())
#print(species_info_data[species_info_data['common_names'] == 'Brachythecium Moss'])
# the common_names is a string variable with the common names of the animal. The most common name is 'Common Name: Brachythecium Moss ' with 7 observations
# exist some common_names that share differents scientific_name, for example Brachythecium digastrum and Brachythecium oedipodium

### conservation_status feature ###
#print(species_info_data.conservation_status.unique())
#print(species_info_data.conservation_status.value_counts())
# the conservation_status is a nominal categorical variable with 5 categories: Species of Concern - 161, Endangered - 16, Threatened - 10, In Recovery - 4 and Nan - 5633

merged_observations_species = pd.merge(observations_data, species_info_data, on='scientific_name', how='inner')
#print(merged_observations_species.head())
#print(merged_observations_species.info())
#print(merged_observations_species.describe())

### Search a significant difference between observations and park_name ###
# Great Smoky Mountains National Park, Yosemite National Park, Bryce National Park and Yellowstone National Park
great_smoky_mountains = merged_observations_species[merged_observations_species['park_name'] == 'Great Smoky Mountains National Park']
yosemite = merged_observations_species[merged_observations_species['park_name'] == 'Yosemite National Park']
bryce = merged_observations_species[merged_observations_species['park_name'] == 'Bryce National Park']
yellowstone = merged_observations_species[merged_observations_species['park_name'] == 'Yellowstone National Park']
#print(great_smoky_mountains[great_smoky_mountains.category == 'Mammal'].describe())
#print(yosemite[yosemite.category == 'Mammal'].describe())
#print(bryce[bryce.category == 'Mammal'].describe())
#print(yellowstone[yellowstone.category == 'Mammal'].describe())
# the observations per park are equals but the mean of observations per category are differents

# Observe the difference between any park and the categories of the animals creating a side by side bar plot
#print(great_smoky_mountains.groupby('category').observations.mean())
#print(yosemite.groupby('category').observations.mean())
#print(bryce.groupby('category').observations.mean())
#print(yellowstone.groupby('category').observations.mean())
great_smoky_categ_means = great_smoky_mountains.groupby('category').observations.mean()
yosemite_categ_means = yosemite.groupby('category').observations.mean()
bryce_categ_means = bryce.groupby('category').observations.mean()
yellowstone_categ_means = yellowstone.groupby('category').observations.mean()

n = 1 # This is our first dataset (out of 4)
t = 4 # Number of datasets
d = 7 # Number of sets of bars
w = 0.8 # Width of each bar
x_values = [t*element + w*n for element in range(d)]
plt.bar(x_values, great_smoky_categ_means, label='Great Smoky Mountains National Park')
n = 2 # This is our second dataset (out of 4)
x_values = [t*element + w*n for element in range(d)]
plt.bar(x_values, yosemite_categ_means, label='Yosemite National Park')
n = 3 # This is our third dataset (out of 4)
x_values = [t*element + w*n for element in range(d)]
plt.bar(x_values, bryce_categ_means, label='Bryce National Park')
n = 4 # This is our fourth dataset (out of 4)
x_values = [t*element + w*n for element in range(d)]
plt.bar(x_values, yellowstone_categ_means, label='Yellowstone National Park')
plt.legend()
plt.title('Number of observations per category and park')
plt.xlabel('Category')
plt.ylabel('Number of observations')
plt.xticks([t*element + w for element in range(d)], great_smoky_mountains.category.unique())
plt.savefig('observations_per_category_park.png')
#plt.show()
#plt.clf()

# Observe the differences among the conservation status and categories of the animals
#print(merged_observations_species.conservation_status.value_counts())  
#print(merged_observations_species.groupby('category').conservation_status.value_counts())
species_of_concern = merged_observations_species[merged_observations_species['conservation_status'] == 'Species of Concern']
endangered = merged_observations_species[merged_observations_species['conservation_status'] == 'Endangered']
threatened = merged_observations_species[merged_observations_species['conservation_status'] == 'Threatened']
in_recovery = merged_observations_species[merged_observations_species['conservation_status'] == 'In Recovery']
print(endangered.groupby('category').conservation_status.count())
print(threatened.groupby('category').conservation_status.count())
print(in_recovery.groupby('category').conservation_status.count())
print(species_of_concern.groupby('category').conservation_status.count())


protected_animals = merged_observations_species.fillna('Not protected')
protected_animals = protected_animals[protected_animals.conservation_status != 'Not protected']
protected_animals = protected_animals.groupby(['category', 'conservation_status']).scientific_name.count().unstack()
protected_animals.fillna(0, inplace=True)

# The animal category with the most protected are Birds, Vascular Plants and Mammals


