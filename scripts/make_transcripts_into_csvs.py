import pandas as pd
import os
import argparse
import re

def make_df(filename):
    transcript_text = open(filename, 'r')
    names = []
    dialogs = []
    previous_name = None
    for line in transcript_text:
        line = line.strip()
        # get rid of lines we don't want
        if line == "":
            continue # empty line
        if ((line[0] == '(' and line[-1] == ')') or (line[0] == '[' and line[-1] == ']') or
            (line[:3] == '**(' and line[-3:] == ')**') or (line[:3] == '**[' and line[-3:] == ']**')):
            continue # description line
        if ("end credits" in line.lower() or line == 'Prologue' or line == 'Introduction' 
            or line == 'THE END' or line.split(" ")[0] == 'Part' or line.split(" ")[0] == 'Act'):
            continue
        if '♪' in line:
            continue # we're skipping all song lines
        # remove anything that is of the form **(Song: smt)** (Song: smt)
        line = re.sub(r'\*\*\(Song: [^)]*\)\*\*', '', line).strip()
        line = re.sub(r'\(Song: [^)]*\)', '', line).strip()

        # now find the dialog
        if line.startswith('**'):
            # find other end
            end_index = line.find('**', 2)
            # we need need to check with : is, since sometimes it's bolded sometimes not
            colon_index = line.find(':')
            if colon_index < end_index:
                name = line[2:end_index-1].strip()
                dialog = line[end_index + 2:].strip().strip().replace('\u00a0', ' ') # the replace is due a weird space symbol in some of the transcripts
            else:
                name = line[2:end_index].strip()
                dialog = line[end_index + 3:].strip().strip().replace('\u00a0', ' ')
            previous_name = name
        else:
            # then take the previous speaker's name (sometimes it does this, new line, same speaker)
            name = previous_name
            dialog = line.strip().replace('\u00a0', ' ')

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
        if i == 5:
            pass
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