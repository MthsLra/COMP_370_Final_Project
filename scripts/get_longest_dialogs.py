import pandas as pd
import os
import argparse


def longest_dialogues(df, n):
    df = df.copy()
    # remove parenthesis
    df['Dialog No Paren'] = df['Dialog'].str.replace(r'(\([^)]*\))', '', regex=True)
    df['Dialog No Paren'] = df['Dialog No Paren'].str.replace(r'\s{2,}', ' ', regex=True).str.strip()

    # sort the dialogue by length
    longest = df.loc[df['Dialog No Paren'].str.len().nlargest(n).index]
    return longest[['Name', 'Dialog']]

def get_longest_dialogues_csv(df, char_name, exclude, longest_dialog_folder, n):
    exclude_char = exclude.get(char_name, [])
    print(exclude_char)

    names = df['Name'].unique()
    names_filtered = list(filter(lambda name: char_name in str(name).lower(), names))
    names_filtered = [name for name in names_filtered if name not in exclude_char]
    for i in names_filtered:
        print(i)
    print(len(names_filtered))

    filtered_df = df[df['Name'].isin(names_filtered)]
    print(len(filtered_df))
    longest_diags = longest_dialogues(filtered_df, n)

    if not os.path.exists(longest_dialog_folder):
        os.makedirs(longest_dialog_folder)

    filepathname = os.path.join(longest_dialog_folder, f'{char_name.replace(" ", "_")}_longest_dialogue.csv')
    # filepathname = os.path.join(longest_dialog_folder, f'{char_name.replace(" ", "_")}_all_dialogue.csv')
    longest_diags.to_csv(filepathname, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, help="number of lines")
    parser.add_argument("longest_dialog_folder", type=str, help="name of folder to put longest_dialogs")
    parser.add_argument("transcript", type=str, help="pathname to transcript")
    parser.add_argument("excluded_names", type=str, help="txt file with names to exclude")
    parser.add_argument("-n", "--name", type=str, help="name of target person", default=None)

    args = parser.parse_args()

    df = pd.read_csv(args.transcript)

    exclude = {}
    current_name = None
    with open(args.excluded_names, 'r') as f:
        for line in f:
            if line[0] == "#":
                current_name = line.strip().replace('#', '')
                exclude[current_name] = []
            else:
                exclude[current_name].append(line.strip())

    if args.name is None:
        # then we do everything in the dictionary
        for name in exclude.keys():
            get_longest_dialogues_csv(df, name, exclude, args.longest_dialog_folder, args.n)
    else:
        # then we do the given name only
        get_longest_dialogues_csv(df, args.name.lower(), exclude, args.longest_dialog_folder, args.n)
    


if __name__ == "__main__":
    main()