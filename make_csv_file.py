import pandas as pd
import os

def make_df(filename):
    script = open(filename, 'r')
    names = []
    dialogs = []
    previous_name = None
    for line in script:
        if line.strip() == "":
            continue # empty line
        if (line.strip()[0] == '(' and line.strip()[-1] == ')') or (line.strip()[0] == '[' and line.strip()[-1] == ']'):
            continue # description line
        if ("end credits" in line.strip().lower() or line.strip() == 'Prologue' or line.strip() == 'Introduction' 
            or line.strip() == 'THE END' or line.strip().split(" ")[0] == 'Part' or line.strip().split(" ")[0] == 'Act'):
            continue
        if line.strip() == 'Contents[show]':
            continue # errors in dialog txt
        if '♪' in line.strip():
            continue # we're skipping all song lines
        # now split the name: dialog
        split_line = line.strip().split(":")
        # if len(split_line) == 1:
        #     print(f'error in file {filename}: {line}')
        #     continue
        if len(split_line) == 1:
            name = previous_name
            dialog = split_line[0].strip().replace('\u00a0', ' ')
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
    df = pd.DataFrame(data)
    pathname = filename.split(os.sep)
    if not os.path.exists('transcripts_csvs'):
        os.makedirs('transcripts_csvs')
    if not os.path.exists(os.path.join('transcripts_csvs', pathname[-2])):
        os.makedirs(os.path.join('transcripts_csvs', pathname[-2]))
    csv_file_name = os.path.join('transcripts_csvs', pathname[-2], f'{pathname[-1].replace(".txt","")}.csv')
    df.to_csv(csv_file_name, index=False)


def main():
    for i in range(1,5):
        for j in range(1,65):
            filename = os.path.join('transcripts_txt',f'season_{i}',f'episode{j}.txt')
            if os.path.exists(filename):
                make_df(filename)

if __name__ == "__main__":
    main()