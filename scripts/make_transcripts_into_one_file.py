import pandas as pd
import os
import argparse




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_folder_name", type=str, help="folder name with csv files")
    parser.add_argument("one_file_csv_name", type=str, help="name of file to put the whole transcript")

    args = parser.parse_args()

    # get all the csv files in an array
    all_files = []
    for i in range(1,6):
        for j in range(1, 65):
            filename = os.path.join(args.csv_folder_name,f'season{i}', f"episode{j}.csv")
            # if this episode exists (there aren't 65 episodes in each season)
            if os.path.exists(filename):
                all_files.append((filename,i,j))
    
    # make a list of df's to concat
    df_list = []
    for (f, season, episode) in all_files:
        # make csv into a csv
        file_df = pd.read_csv(f)
        # add a column for season and episode numbers
        file_df['Season'] = season
        file_df['Episode'] = episode
        # reorder the columns
        file_df = file_df[['Season', 'Episode', 'Name', 'Dialog']]
        df_list.append(file_df)

    # now concatenate all of these df's
    df = pd.concat(df_list, ignore_index=True)
    df.to_csv(args.one_file_csv_name, index=False)
    # df['Name'].value_counts().to_csv("name_value_counts.csv")


if __name__ == "__main__":
    main()