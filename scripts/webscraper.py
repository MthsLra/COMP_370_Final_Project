import argparse
from bs4 import BeautifulSoup
import os
import requests
import time


def get_transcript_html(url):
    transcript_url = url + "/Transcript"
    r = requests.get(transcript_url)
    r.raise_for_status()
    time.sleep(0.5)
    html_text = r.text
    return html_text

def get_transcript_text(html_text):
    soup = BeautifulSoup(html_text, "html.parser") 

    transcript_panel = soup.select_one('div.mw-content-ltr.mw-parser-output')

    ps = transcript_panel.select('p') # all text is in a <p> 

    transcript_text = ""
    for p in ps:
        # first find all of the <br>'s 
        # these are sometimes use as line breaks instead of \n
        for br in p.find_all('br'): 
            br.replace_with('\n')
        # now add the text
        transcript_text += p.text + "\n"

    return transcript_text



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("transcripts_folder_name", type=str, help="folder name with transcripts and contains season_x_urls.txt for each season")

    args = parser.parse_args()

    
    # go season by season:
    for i in range(1,6):
        # check that the folder seasoni exists
        season_folder_path = os.path.join(args.transcripts_folder_name, f'season{i}')
        if not os.path.exists(season_folder_path):
            os.makedirs(season_folder_path)

        # open up season_i_urls.txt
        urls_file = os.path.join(args.transcripts_folder_name, f'season_{i}_urls.txt')
        with open(urls_file, 'r') as f:
            # each line is a link to the episode
            episode_num = 1
            for line in f:
                htmltext = get_transcript_html(line.strip())
                text = get_transcript_text(htmltext)
                # add to a file
                file_path = os.path.join(season_folder_path, f'episode{episode_num}.txt')
                with open(file_path, 'w') as f_ep:
                    f_ep.write(text)
                episode_num += 1
                print(f'Wrote file {file_path}')






if __name__ == "__main__":
    main()
