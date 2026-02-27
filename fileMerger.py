#!/usr/bin/env python
# coding: utf-8

"""
================================================================================
IMAGE FEATURE DATASET MERGER
================================================================================
Authors: Giuseppe Riccio, Stefano Cavuoti
Date: 2026-02-24
Description:
    This script automates the merging of multiple CSV datasets containing 
    standard image features, Haralick textures, and Haar-like features.
    
    Key functionalities:
    1. Scans specific directories for CSV files.
    2. Renames columns dynamically by prefixing them with the source filename
       to prevent name collisions and maintain traceability.
    3. Concatenates datasets horizontally (axis=1) based on the assumption 
       of matching row indices.
    4. Generates an output file with a suffix indicating which feature sets 
       (Haralick/Haar) were included in the final merge.

Dependencies:
    - pandas
    - os

Usage:
    - Ensure '2kyr_new/', 'haralick_files/', and 'haar_files/' directories exist.
    - Set 'merge_haralick' and 'merge_haar' flags to True/False as needed.
================================================================================
"""        


import os
import pandas as pd

# Folder containing the source CSV files
folder_path = '2kyr_new' + os.sep
# print(os.listdir(folder_path))

# Folder containing Haralick feature files
folder_haralick = 'haralick_files' + os.sep

# Folder containing Haar-like feature files
folder_haarlike = 'haar_files' + os.sep

# Get the list of CSV files in the folder, sorted alphabetically


                                                                        
csv_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv')])

if not csv_files:
    print("No CSV files found in the specified folder.")

# List to store the DataFrames
dfs = []

# Read each CSV file and append the filename to the column names
for file in csv_files:
    # for file in [csv_files[0]]:
    file_path = os.path.join(folder_path, file)
    print("Merging: " + file_path)
    try:
        df = pd.read_csv(file_path)
        
        if df.empty:
            print(f"The file {file} is empty. Skipping.")
            continue
        
        # Get filename without extension
        file_name = os.path.splitext(file)[0]
        
        # Rename columns by adding the filename prefix
        df.columns = [f"{file_name}_{col}" for col in df.columns]
        
        dfs.append(df)
    except Exception as e:
        print(f"Error reading file {file}: {str(e)}")

if not dfs:
    print("No valid DataFrames to merge. Ensure CSV files are not empty and are readable.")
    exit(1)

# Flags to control feature merging
merge_haralick = True
merge_haar = False    

# Haralick files processing
                      
               
if merge_haralick:
    if os.path.isdir(folder_haralick):
        haralick_files = sorted([f for f in os.listdir(folder_haralick) if f.endswith('.csv')]) 
        print("\nMerging Haralick files...")
                    
        for harafile in haralick_files:
            harafile_path = os.path.join(folder_haralick, harafile)
            print("\tAdding: " + harafile_path)
            try:
                dfh = pd.read_csv(harafile_path)
                if dfh.empty:
                    print(f"The file {harafile} is empty. Skipping.")
                    continue
                
                # Get filename without extension and remove specific suffix
                file_name_h = os.path.splitext(harafile)[0].replace("_haralick", "")

                # Rename columns by adding the filename prefix
                dfh.columns = [f"{file_name_h}_{col}" for col in dfh.columns]                        
                                                     
                dfs.append(dfh)
            except Exception as e:
                print(f"Error reading file {harafile}: {str(e)}")
            
    else:
        print("No directory found for Haralick features")    
    
# Haar-like files processing
if merge_haar:
    if os.path.isdir(folder_haarlike):
        haarfiles = sorted([f for f in os.listdir(folder_haarlike) if f.endswith('.csv')]) 
        print("\nMerging Haar-like files...")
        for haarfile in haarfiles:
                                                                             
            print(haarfile)
            haarfile_path = os.path.join(folder_haarlike, haarfile)
            print("\tAdding: " + haarfile_path)
            try:
                dfh = pd.read_csv(haarfile_path)
                if dfh.empty:
                    print(f"The file {haarfile} is empty. Skipping.")
                    continue
                
                # Get filename without extension and remove specific suffix
                file_name_h = os.path.splitext(haarfile)[0].replace("_haar", "")

                # Rename columns by adding the filename prefix
                dfh.columns = [f"{file_name_h}_{col}" for col in dfh.columns]                        
                                                     
                dfs.append(dfh)
            except Exception as e:
                print(f"Error reading file {haarfile}: {str(e)}")    
    else:
        print("No directory found for Haar-like features") 
        
# Combine all DataFrames along the columns axis
print("Saving Final Dataset...")
merged_df = pd.concat(dfs, axis=1)

# Determine the suffix based on which features were merged
if merge_haralick and merge_haar:
    suffix = '_AllColumns_imgfeatures'
elif merge_haralick and not merge_haar:
    suffix = '_AllColumns_onlyHaralick'
elif not merge_haralick and merge_haar:
    suffix = '_AllColumns_onlyHaar'
else:
    suffix = '_AllColumns'

# Save the merged DataFrame to a new CSV file
output_filename = folder_path[:-1] + suffix + '.csv'
merged_df.to_csv(output_filename, index=False)

print("CSV files merged successfully!")


        




