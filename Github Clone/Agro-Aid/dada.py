import os
import shutil
import random

# Define the path to the dataset and the new directories for train and validation sets
dataset_path = r"C:\GitHubRepo\Agro-Aid\Crop_Diseases"
train_path = r"C:\GitHubRepo\Agro-Aid\Crop_Diseases_train"
val_path = r"C:\GitHubRepo\Agro-Aid\Crop_Diseases_val"

# Create the directories for train and validation if they don't exist
os.makedirs(train_path, exist_ok=True)
os.makedirs(val_path, exist_ok=True)

# Iterate through each folder in the dataset
for folder_name in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder_name)

    if os.path.isdir(folder_path):  # Check if it's a directory
        # Create train and validation subfolders for the current folder
        train_folder = os.path.join(train_path, folder_name)
        val_folder = os.path.join(val_path, folder_name)
        os.makedirs(train_folder, exist_ok=True)
        os.makedirs(val_folder, exist_ok=True)

        # Get all files in the folder
        files = os.listdir(folder_path)
        
        # Shuffle the files and split into 80-20 ratio
        random.shuffle(files)
        split_index = int(len(files) * 0.8)
        
        # Move the files into respective folders
        for i, file in enumerate(files):
            file_path = os.path.join(folder_path, file)
            if i < split_index:
                shutil.copy(file_path, os.path.join(train_folder, file))  # Move to train
            else:
                shutil.copy(file_path, os.path.join(val_folder, file))  # Move to validation
