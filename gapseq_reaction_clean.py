#!/bin/python

# Author: Marie-Madlen Pust 
# pust.marie-madlen@mh-hannover.de
# 03 March 2020
# Work with gapseq SLURM output

import pandas as pd
import os
import sys

current_directory = os.getcwd()

with open(sys.argv[1],"r") as input_file:
    lines = input_file.readlines()
    
    which_genome = []
    pathway_id = []
    pathway_reaction = []
    pathway_completeness_perc = []
    pathway_completeness = []
    pathway_candidate_reaction = []
    pathway_key_reactions = []

    for line in lines:
        if "Checking for pathways and reactions in" in line:
            line_clean0 = line.rsplit('Checking for pathways and reactions in: ')[1]
            line_clean1 = line_clean0.rsplit('.')[0]
            which_genome.append(line_clean1)
    
        elif "Checking for pathway " in line:
            line_clean0 = line.rsplit('Checking for pathway ')[1]
            line_clean1 = line_clean0.rsplit(' with ')[0]
            
            if "|" in line_clean1:
                line_id0 = line_clean1.rsplit('| ')[0]
                line_id1 = line_id0.rsplit('|')[1]
                pathway_id.append(line_id1)
                line_clean2 = line_clean1.rsplit('| ')[1]
                pathway_reaction.append(line_clean2)          
            else:
                line_id0 = line_clean1.rsplit(' ')[1]
                pathway_id.append(line_id1)
                line_clean2 = line_clean1.rsplit(' ')[1]
                pathway_reaction.append(line_clean2)
            
        elif "Pathway completeness:" in line:
            line_clean0 = line.rsplit('Pathway completeness: ')[1]
            line_clean1 = line_clean0.rsplit('\n')[0]
            line_clean_perc0 = line_clean1.rsplit(' ')[1]
            pathway_completeness_perc.append(line_clean_perc0)
            line_clean2 = line_clean1.rsplit(' ')[0]
            pathway_completeness.append(line_clean2)
    
        elif "Hits with candidate reactions in database:" in line:
            line_clean0 = line.rsplit('Hits with candidate reactions in database:')[1]
            line_clean1 = line_clean0.rsplit('\n')[0]
            pathway_candidate_reaction.append(line_clean1)
    
        elif"Key reactions:" in line:
            line_clean0 = line.rsplit('Key reactions: ')[1]
            line_clean1 = line_clean0.rsplit('\n')[0]
            pathway_key_reactions.append(line_clean1)
        else:
            next

    combine_all_df = pd.DataFrame(pathway_id, columns=['pathway_id'])
    combine_all_df['pathway_reaction'] = pathway_reaction
    combine_all_df['pathway_completeness_perc'] = pathway_completeness_perc
    combine_all_df['pathway_completeness_perc'] = combine_all_df['pathway_completeness_perc'].str.replace('(', '')
    combine_all_df['pathway_completeness_perc'] = combine_all_df['pathway_completeness_perc'].str.replace(')', '')
    combine_all_df['pathway_completeness_perc'] = combine_all_df['pathway_completeness_perc'].str.replace('%', '')
    combine_all_df['pathway_completeness'] = pathway_completeness
    combine_all_df['pathway_candidate_reaction'] = pathway_candidate_reaction
    combine_all_df['pathway_key_reactions'] = pathway_key_reactions

    genome_name = which_genome[0]
    current_directory = os.getcwd()
    combine_all_df.to_csv(current_directory + '/' + genome_name + '_pathways_reactions.csv', 
                      sep=";", header=True, index=False)
