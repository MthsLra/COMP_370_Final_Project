import pandas as pd
import os
import argparse

def make_df(filename):
    transcript_text = open(filename, 'r')
    names = []
    dialogs = []
    previous_name = None
    for line in transcript_text:
        # get rid of lines we don't want
        if line.strip() == "":
            continue # empty line
        if (line.strip()[0] == '(' and line.strip()[-1] == ')') or (line.strip()[0] == '[' and line.strip()[-1] == ']'):
            continue # description line
        if ("end credits" in line.strip().lower() or line.strip() == 'Prologue' or line.strip() == 'Introduction' 
            or line.strip() == 'THE END' or line.strip().split(" ")[0] == 'Part' or line.strip().split(" ")[0] == 'Act'):
            continue
        if '♪' in line.strip():
            continue # we're skipping all song lines

        # now split the name: dialog
        split_line = line.strip().split(":")

        # if len(split_line) == 1:
        #     print(f'error in file {filename}: {line}')
        #     continue
        if len(split_line) == 1:
            name = previous_name
            dialog = split_line[0].strip().replace('\u00a0', ' ') # the replace is due a weird space symbol in some of the transcripts
        else:
            name = split_line[0].strip()
            previous_name = name
            dialog = split_line[1].strip().replace('\u00a0', ' ')

        names.append(name)
        dialogs.append(dialog)

    data = {
        'Name': names,
        'Dialog': dialogs
    }

    # make into a dataframe
    df = pd.DataFrame(data)

    return df



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("txt_folder_name", type=str, help="folder name where txt files are")
    parser.add_argument("csv_folder_name", type=str, help="folder name to put csv files in")

    args = parser.parse_args()

    # go through all of the episodes
    for i in range(1,6):
        for j in range(1,65):
            filename = os.path.join(args.txt_folder_name,f'season{i}',f'episode{j}.txt')
            # if the episode exists, make it into a csv (there aren't 65 episodes in each season)
            if os.path.exists(filename):
                # put this into a dataframe
                df = make_df(filename)
                # add this as a csv file
                # check that csv folder exists 
                if not os.path.exists(args.csv_folder_name):
                    os.makedirs(args.csv_folder_name)
                # check that the season folder exists
                if not os.path.exists(os.path.join(args.csv_folder_name, f'season{i}')):
                    os.makedirs(os.path.join(args.csv_folder_name, f'season{i}'))
                # make the csv file
                csv_file_name = os.path.join(args.csv_folder_name, f'season{i}', f'episode{j}.csv')
                df.to_csv(csv_file_name, index=False)


if __name__ == "__main__":
    main()