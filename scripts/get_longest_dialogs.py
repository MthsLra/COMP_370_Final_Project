import pandas as pd
import os
import argparse


def longest_dialogues(df, n):
    # remove parenthesis
    df.loc[:, 'Dialog'] = df['Dialog'].str.replace(r'(\([^)]*\))', '', regex=True)
    df.loc[:, 'Dialog'] = df['Dialog'].str.replace(r'\s{2,}', ' ', regex=True).str.strip()

    # sort the dialogue by length
    longest = df.loc[df['Dialog'].str.len().nlargest(n).index]
    return longest[['Name', 'Dialog']]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=str, help="number of lines")
    parser.add_argument("longest_dialog_folder", type=str, help="name of folder to put longest_dialogs")
    parser.add_argument("transcript", type=str, help="pathname to transcript")
    parser.add_argument("excluded_names", type=str, help="txt file with names to exclude")
    parser.add_argument("name", type=str, help="name of target person")

    args = parser.parse_args()

    df = pd.read_csv(args.transcript)

    exclude = []
    with open(args.excluded_names, 'r') as f:
        for line in f:
            exclude.append(line.strip())
    char_name = args.name.lower()

    names = df['Name'].unique()
    names_filtered = list(filter(lambda name: args.name in str(name).lower(), names))
    names_filtered = [name for name in names_filtered if name not in exclude]
    for i in names_filtered:
        print(i)
    print(len(names_filtered))

    filtered_df = df[df['Name'].isin(names_filtered)]
    print(len(filtered_df))
    longest_diags = longest_dialogues(filtered_df, 350)

    filepathname = os.path.join(args.longest_dialog_folder, f'{args.name}_longest_dialogue.csv')
    longest_diags.to_csv(filepathname, index=False)
    


if __name__ == "__main__":
    main()