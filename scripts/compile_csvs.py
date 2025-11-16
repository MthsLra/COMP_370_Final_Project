import pandas as pd
import os
import glob

### This is also very exploratory code and just a whole bunch of things are here lol

def longest_dialogues(df, n):
    # Sort dialogues by length of the 'Dialog' column
    longest = df.loc[df['Dialog'].str.len().nlargest(n).index]
    return longest[['Name', 'Dialog']]

def main():
    all_files = []
    for i in range(1,5):
        for j in range(1, 65):
            filename = os.path.join('phineas_and_ferb_csvs',f'season_{i}', f"episode{j}.csv")
            if os.path.exists(filename):
                all_files.append(filename)
    
    df_list = []
    for f in all_files:
        temp_df = pd.read_csv(f)
        pathname = f.split(os.sep)
        season = int(pathname[-2].replace("season_", ""))
        episode = int(pathname[-1].replace("episode", "").replace(".csv", ""))
        temp_df['Season'] = season
        temp_df['Episode'] = episode
        temp_df = temp_df[['Season', 'Episode', 'Name', 'Dialog']]
        df_list.append(temp_df)
    df = pd.concat(df_list, ignore_index=True)
    # df.to_csv('phineas_and_ferb_csvs/compiled_transcript.csv', index=False)
    df['Name'].value_counts().to_csv("name_value_counts.csv")

    # baljeetdf = df[df['Name'] == 'Baljeet']
    # print(len(baljeetdf))
    # longest_diags = longest_dialogues(baljeetdf, 300)
    # longest_diags.to_csv('baljeetlongestdialogues.csv', index=False)

    # names = df['Name'].unique()
    # namewbaljeet = list(filter(lambda name: 'baljeet' in str(name).lower(), names))
    # # print(list(namewbaljeet))

    # baljeetdf = df[df['Name'].isin(namewbaljeet)]
    # print(len(baljeetdf))
    # longest_diags = longest_dialogues(baljeetdf, 300)
    # longest_diags.to_csv('baljeetlongestdialogues3.csv', index=False)

    # names = df['Name'].unique()
    # names_filtered = list(filter(lambda name: 'ferb' in str(name).lower(), names))
    # names_filtered.remove('Ferbettes')
    # names_filtered.remove('Everyone but Ferb')
    # names_filtered.remove('All but Ferb')
    # names_filtered.remove("Ferb's cousin")
    # names_filtered.remove("(Phineas, Ferb, and Perry ride in on the same chairs Doofenshmirtz did)Phineas")
    # # count = 0
    # # for i in names_filtered:
    # #     print(count)
    # #     print(i)
    # #     count+=1

    # filtered_df = df[df['Name'].isin(names_filtered)]
    # print(len(filtered_df))
    # longest_diags = longest_dialogues(filtered_df, 300)
    # filtered_df.to_csv('ferb_dialogue.csv', index=False)

    names = df['Name'].unique()
    names_filtered = list(filter(lambda name: 'vanessa' in str(name).lower(), names))

    filtered_df = df[df['Name'].isin(names_filtered)]
    print(len(filtered_df))
    longest_diags = longest_dialogues(filtered_df, 350)
    longest_diags.to_csv('longest_dialogs/vanessa_longest_dialogue.csv', index=False)

    # for i in range(1,5):
    #     for j in range(1,65):
    #         filename = os.path.join('phineas_and_ferb_csvs',f'season_{i}',f'episode{j}.txt')
    #         if os.path.exists(filename):
    #             make_df(filename)

if __name__ == "__main__":
    main()