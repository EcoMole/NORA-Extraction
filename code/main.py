import pandas as pd
import os
from opinion import Opinion
import typing
from category_extractor import OpinionAExtraction, OpinionBExtraction, OpinionCExtraction, OpinionDExtraction, OpinionEExtraction

def get_opinions(root_dir: str) -> typing.List[Opinion]:
    opinions: typing.List[Opinion] = []
    data_info = pd.read_csv('../outputs/data_info.csv')
    data_tuples = zip(data_info['question'], data_info['group'], data_info['type'])

    for data_tuple in data_tuples:
        if data_tuple[2] != 'opinion': # we only want opinions, not guidances etc.
            continue
        question_path = os.path.join(root_dir, data_tuple[0])
        print(question_path)
        for root, _, files in os.walk(question_path):
            for file in files:
                if file.endswith('.tei.xml'):
                    tei_file = os.path.join(root, file)
                if file.endswith('.xml') and not file.endswith('.tei.xml'):
                    xml_file = os.path.join(root, file)

        if xml_file is not None: #TODO better
                if data_tuple[1] == 'A':
                    opinions.append(Opinion(xml_file, tei_file, OpinionAExtraction()))
                elif data_tuple[1] == 'B':
                        opinions.append(Opinion(xml_file, tei_file, OpinionBExtraction()))
                elif data_tuple[1] == 'C':
                    opinions.append(Opinion(xml_file, tei_file, OpinionCExtraction()))
                elif data_tuple[1] == 'D':
                    opinions.append(Opinion(xml_file, tei_file, OpinionDExtraction()))
                elif data_tuple[1] == 'E':
                    opinions.append(Opinion(xml_file, tei_file, OpinionEExtraction()))
    return opinions


def main():
    opinions = get_opinions('../../NFs/')
    print(f' {len(opinions)} opinions created')
    dfs = [opinion.into_df() for opinion in opinions]
    df = pd.concat(dfs)
    print(df.head())
    #get not null categories:
    print(len(df))
    # get categories that are not '':
    print(len(df[df['categories'] != '']))

    df.to_csv('../outputs/test_output.csv')


if __name__=="__main__": 
    main() 
