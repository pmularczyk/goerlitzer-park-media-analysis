# Standard library imports
import json
import re
from os import path, listdir, mkdir
from os.path import dirname, exists
from pathlib import Path
from collections import Counter
from itertools import chain, groupby
from operator import itemgetter
from pprint import pprint

# Third party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud

# Local application imports
from utils.utils import remove_umlaute
from client.client import Client

def create_directory(img_json):
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent
    articles = project_path.joinpath("resources").joinpath("articles")
    for dir_name in listdir(articles):
        directory = create_path(img_json, dir_name)
        # Create target Directory if don"t exist
        if not exists(directory):
            mkdir(directory)
            print("Directory " , directory ,  " Created ")
        else:    
            print("Directory " , directory ,  " already exists")

def create_path(img_json, source):
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent
    output_path = project_path.joinpath("out").joinpath(img_json).joinpath(source)
    return output_path

def load_file():
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent
    resources = project_path.joinpath("resources").joinpath("stopwords")
    stopwords_path = resources.joinpath("german_stopwords_plain.txt")
    return stopwords_path

def load_stopwords():
    with open(load_file(), "r", encoding="utf-8") as file:
        lowercase = [remove_umlaute(line.strip()) for line in file if not line.startswith(";")]
        capitalized = [word.capitalize() for word in lowercase]
        stopwords = lowercase + capitalized
        return stopwords

def get_output_path(img_json, source, filename):
    current = Path(dirname(__file__)).absolute()
    project_path = current.parent
    resources = project_path.joinpath("out").joinpath(img_json).joinpath(source)
    output_path = resources.joinpath(filename)
    return output_path

def get_data_as_json():
    client = Client()
    df = client.get_current_entries()
    
    output = list()
    for row, col in df.iterrows():
        obj = {
            "id": col["id"],
            "date": col["date"],
            "place": col["place"],
            "original": col["original"],
            "source": col["source"],
            "tag": col["tag"],
            "title": col["title"],
            "subtitle": col["subtitle"],
            "author": col["author"],
            "article": col["article"],
            "additional": col["additional"],
            "link": col["link"]
        }
        output.append(obj)
    return output

def get_analysis_over_all_articles():

    words_from_all_articles = list()
    sentences_from_all_articles = list()
    titles_from_all_articles = list()
    data = get_data_as_json()
    number_of_articles = len(data)

    for element in data:
        all_words = element["article"].split(" ")
        all_words = list(filter(None, all_words))
        words_from_all_articles.append(all_words)

        sentences = element["article"].split(".")
        sentences = list(filter(None, sentences))
        sentences_from_all_articles.append(sentences)

        repl_pattern = "\W+"

        title = "" if element["title"] is None else element["title"]
        subtitle = "" if element["subtitle"] is None else element["subtitle"]

        if title == "" and subtitle == "" and element["source"] == "Twitter":
            continue
        elif title == "" and subtitle == "" and element["source"] != "Twitter":
            continue
        else:
            theme = title + " " + subtitle
        titles_from_all_articles.append(theme)
            

    words_from_all_articles = list(chain.from_iterable(words_from_all_articles))
    sentences_from_all_articles = list(chain.from_iterable(sentences_from_all_articles))
    number_of_sentences = len(sentences_from_all_articles)

    titles_from_all_articles = [title.split(" ") for title in titles_from_all_articles]
    titles_from_all_articles = list(chain.from_iterable(titles_from_all_articles))
    words_from_titles_from_all_articles = list(filter(None, titles_from_all_articles))

    word_count_from_titles = len(words_from_titles_from_all_articles)
    number_of_words = len(words_from_all_articles)
    stopwords = load_stopwords()
    remaining_words_all_articles = [elem for elem in words_from_all_articles if elem not in stopwords]
    remaining_words_from_titles = [elem for elem in words_from_titles_from_all_articles if elem not in stopwords]
    number_of_remaining_words = len(remaining_words_all_articles)
    word_count_remaining_from_titles = len(remaining_words_from_titles)


    counted_words_all_articles = Counter(remaining_words_all_articles)
    counted_words_from_titles = Counter(remaining_words_from_titles)
    most_common_json = {key: value for key, value in counted_words_all_articles.most_common(100)}
    most_common_json_from_titles = {key: value for key, value in counted_words_from_titles.most_common(100)}

    df = pd.DataFrame(counted_words_all_articles.most_common(25), columns=["word", "count"])
    ax = df.plot.barh(x="word", y="count", figsize=(22, 12))
    plt.grid(axis="x", alpha=0.55)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=16)
    plt.title("Word count of most frequent words\n over all articles", fontsize=22)
    plt.ylabel("Most frequent words", fontsize=20)
    plt.xlabel("Count", fontsize=20)
    ax.invert_yaxis()
    for i, v in enumerate(df["count"]):
        ax.text(v + 3, i + .25, "Count: " + str(v), fontsize=15, color='dimgrey')
    plt.savefig(get_output_path("img", "", "word_count_all_articles.png"), dpi=300, orientation="landscape")

    df = pd.DataFrame(counted_words_from_titles.most_common(25), columns=["word", "count"])
    ax = df.plot.barh(x="word", y="count", figsize=(22, 12))
    plt.grid(axis="x", alpha=0.55)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=16)
    plt.title("Word count of most frequent words\n from all titles", fontsize=22)
    plt.ylabel("Most frequent words", fontsize=20)
    plt.xlabel("Count", fontsize=20)
    ax.invert_yaxis()
    for i, v in enumerate(df["count"]):
        ax.text(v + 3, i + .25, "Count: " + str(v), fontsize=15, color='dimgrey')
    plt.savefig(get_output_path("img", "", "word_count_from_titles.png"), dpi=300, orientation="landscape")

    output = {
        "number_of_articles": number_of_articles,
        "initial_number_of_words": number_of_words,
        "average_number_of_words_per_article": round(number_of_words/number_of_articles, 2),
        "number_of_words_after_filtering": number_of_remaining_words,
        "ratio_remaining_words_to_initial_number": round(number_of_remaining_words/number_of_words, 2),
        "number_of_sentences": number_of_sentences,
        "average_number_of_words_per_sentence": round(number_of_words/number_of_sentences, 2),
        "average_number_of_words_after_filtering_per_sentence": round(number_of_remaining_words/number_of_sentences, 2),
        "number_of_words_from_titles": word_count_from_titles,
        "number_of_words_from_titles_after_filtering": word_count_remaining_from_titles
    }

    with open(get_output_path("json", "", "word_count_all_articles.json"), "w") as file:
        json.dump(output, file, indent=4)

    with open(get_output_path("json", "", "most_common_words_all_articles.json"), "w") as file:
        json.dump(most_common_json, file, indent=4)

    with open(get_output_path("json", "", "most_common_words_from_titles.json"), "w") as file:
        json.dump(most_common_json_from_titles, file, indent=4)

    print("Analysis of all articles successful")

def get_analysis():

    mapping = {
        "RTL.de": "rtl_articles", 
        "Welt Print": "welt_articles", 
        "Welt.de": "welt_articles", 
        "ZDF  Markus Lanz": "zdf_articles", 
        "morgenpost.de": "morgenpost_articles", 
        "ZDF  heute.de": "zdf_articles", 
        "ZDF  Zdfzoom": "zdf_articles", 
        "rbb24": "rbb_articles",
        "Tagesspiegel": "tagesspiegel_articles", 
        "Independent.co.uk": "independent_articles", 
        "BZ": "bz_articles", 
        "ZDF  drehscheibe": "zdf_articles", 
        "Twitter": "tweets"
    }

    data = get_data_as_json()
    sources_data = set()
    analysis = list()
    for element in data:
        repl_pattern = "\W+"

        title = "" if element["title"] is None else element["title"]
        subtitle = "" if element["subtitle"] is None else element["subtitle"]

        if title == "" and subtitle == "" and element["source"] == "Twitter":
            theme = str(element["date"]) + "_" + element["author"]
            theme = re.sub("-", "_", theme).lower()
        elif title == "" and subtitle == "" and element["source"] != "Twitter":
            theme = Path(element["link"]).name.replace(".html", "")
            theme = str(element["date"]) + "_" + theme
            theme = re.sub(repl_pattern, "_", theme).lower()
        else:
            theme = str(element["date"]) + "_" + title + " " + subtitle
            theme = re.sub(repl_pattern, "_", theme).lower()

        sentences = element["article"].split(".")
        sentences = list(filter(None, sentences))
        number_of_sentences = len(sentences)

        words_per_sentence = dict()
        for index, word in enumerate(sentences):
            words = word.split(" ")
            words = list(filter(None, words))
            number_of_words = len(words)
            words_per_sentence[index + 1] = number_of_words

        all_words = element["article"].split(" ")
        all_words = list(filter(None, all_words))
        complete_number_words = len(all_words)

        stopwords = load_stopwords()

        # filter out stopwords
        remaining_words = [elem for elem in all_words if elem not in stopwords]
        number_of_remaining_words = len(remaining_words)
        counted_words = Counter(remaining_words)

        out_directory = mapping[element["source"]]

        if title == "" and subtitle == "" and element["source"] == "Twitter":
            filename = "Twitter: " + element["author"]
        elif title == "" and subtitle == "" and element["source"] != "Twitter":
            filename = "ZDF: " + Path(element["link"]).name.replace(".html", "")
        else:
            filename = title + " " + subtitle

        # df = pd.DataFrame(counted_words.most_common(20), columns=["word", "count"])
        # ax = df.plot.barh(x="word", y="count", figsize=(22, 12))
        # plt.grid(axis="x", alpha=0.55)
        # plt.yticks(fontsize=14)
        # plt.xticks(fontsize=16)
        # plt.title("Most frequent words\n {} {}".format(filename, element["date"]), fontsize=18)
        # plt.ylabel("Most frequent words", fontsize=18)
        # plt.xlabel("Count", fontsize=18)
        # ax.invert_yaxis()
        # for i, v in enumerate(df["count"]):
        #     ax.text(v + 3, i + .25, "Count: " + str(v), fontsize=15, color='dimgrey')
        # plt.savefig(get_output_path("img", out_directory, "word_count_{}.png".format(theme)), dpi=300, orientation="landscape")

        # df2 = pd.DataFrame([words_per_sentence])
        # df2 = df2.melt()
        # df2.columns = ["sentence", "word_count"]
        # df2.plot.bar(x="sentence", y="word_count", figsize=(22, 12))
        # plt.grid(axis="y", alpha=0.55)
        # plt.yticks(fontsize=14)
        # plt.xticks(rotation=0, fontsize=12)
        # plt.title("Word count per sentence\n {} {}".format(filename, element["date"]), fontsize=18)
        # plt.ylabel("Words per sentence", fontsize=18)
        # plt.xlabel("Sentence", fontsize=18)
        # plt.savefig(get_output_path("img", out_directory, "words_per_sentence_{}.png".format(theme)), dpi=300, orientation="landscape")

        output = {
            theme: {
            "date": element["date"],
            "place": element["place"],
            "source": element["source"],
            "number_of_sentences": number_of_sentences,
            "number_of_words": complete_number_words,
            "number_of_words_after_filtering": number_of_remaining_words,
            "average_number_of_words_per_sentence": round(complete_number_words/number_of_sentences, 2),
            "average_number_of_words_after_filtering_per_sentence": round(number_of_remaining_words/number_of_sentences, 2)
            }
        }
        analysis.append(output)
        
    #     with open(get_output_path("json", out_directory, "article_analysis_{}.json".format(theme)), "w") as file:
    #         json.dump(output, file, indent=4)

            
    # print("Analysis of individual successful")

def get_grouped_analysis():
    data = get_data_as_json()
    sorted_by_source = sorted(data, key=itemgetter('source'))
    analysis_output_json = list()
    most_common_words_by_groups_json = list()
    title_words_by_groups_json = list()

    for key, value in groupby(sorted_by_source, key=itemgetter('source')):
        articles_per_group = list()
        titles_per_group = list()
        for element in value:
            articles_per_group.append(element["article"])

            title = "" if element["title"] is None else element["title"]
            subtitle = "" if element["subtitle"] is None else element["subtitle"]

            if title == "" and subtitle == "" and element["source"] == "Twitter":
                continue
            elif title == "" and subtitle == "" and element["source"] != "Twitter":
                continue
            else:
                full_title = title + " " + subtitle
            titles_per_group.append(full_title)

        # -------------- Treating words from articles -------------- #
        number_of_articles = len(articles_per_group)
        all_words_by_groups = [element.split(" ") for element in articles_per_group]
        all_words_by_groups = list(chain.from_iterable(all_words_by_groups))
        all_words_by_groups = [re.sub("\W", "", element.lower()) for element in all_words_by_groups]
        all_words_by_groups = list(filter(None, all_words_by_groups))

        number_of_words = len(all_words_by_groups)
        stopwords = load_stopwords()
        remaining_words_by_group = [elem for elem in all_words_by_groups if elem not in stopwords]
        number_of_remaining_words = len(remaining_words_by_group)

        counted_remaining_words_by_groups = Counter(remaining_words_by_group)
        most_common_words_by_groups = (counted_remaining_words_by_groups.most_common(25))
        most_common_by_groups_json = {key: value for key, value in counted_remaining_words_by_groups.most_common(100)}

        all_words_combined_per_group = " ".join(remaining_words_by_group)
        key = key.lower().replace(" ", "_").replace(".de", "")

        # -------------- Treating words from titles -------------- #
        number_of_titles = len(titles_per_group)
        titles_by_groups = [element.split(" ") for element in titles_per_group]
        titles_by_groups = list(chain.from_iterable(titles_by_groups))
        titles_by_groups = [re.sub("\W", "", element.lower()) for element in titles_by_groups]
        titles_by_groups = list(filter(None, titles_by_groups))

        number_of_title_words = len(titles_by_groups)
        remaining_title_words_by_group = [elem for elem in titles_by_groups if elem not in stopwords]
        number_of_remaining_title_words = len(remaining_title_words_by_group)

        counted_remaining_title_words_by_groups = Counter(remaining_title_words_by_group)
        most_common_title_words_by_groups = (counted_remaining_title_words_by_groups.most_common(25))

        most_common_title_words_by_groups_json = {key: value for key, value in counted_remaining_title_words_by_groups.most_common(100)}
        title_words_combined_by_group = " ".join(remaining_title_words_by_group)

        # -------------- Plotting words from articles -------------- #
        # df = pd.DataFrame(most_common_words_by_groups, columns=["word", "count"])
        # ax = df.plot.barh(x="word", y="count", figsize=(22, 12))
        # plt.grid(axis="x", alpha=0.55)
        # plt.yticks(fontsize=14)
        # plt.xticks(fontsize=16)
        # plt.title(f"Word count of most frequent words\n by group: {key}", fontsize=22)
        # plt.ylabel("Most frequent words", fontsize=20)
        # plt.xlabel("Count", fontsize=20)
        # ax.invert_yaxis()
        # for i, v in enumerate(df["count"]):
        #     ax.text(v + 3, i + .25, "Count: " + str(v), fontsize=15, color='dimgrey')
        # plt.savefig(get_output_path("img", "analysis_grouped", f"most_common_words_by_groups_{key}.png"), dpi=300, orientation="landscape")

        # # create wordcloud
        # wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(all_words_combined_per_group)
        # wordcloud2 = WordCloud(width=1600, height=800, background_color="white").generate(all_words_combined_per_group)
        # plt.figure(figsize=(20,10))
        # plt.imshow(wordcloud, interpolation="bilinear")
        # plt.imshow(wordcloud2, interpolation="bilinear")
        # plt.axis("off")
        # plt.tight_layout(pad=0)
        # wordcloud.to_file(get_output_path("img", "analysis_grouped", f"wordcloud_{key}.png"))
        # wordcloud2.to_file(get_output_path("img", "analysis_grouped", f"wordcloud_{key}_v2.png"))

        # -------------- Plotting words from titles -------------- #
        try:
            df = pd.DataFrame(most_common_title_words_by_groups, columns=["word", "count"])
            ax = df.plot.barh(x="word", y="count", figsize=(22, 12))
            plt.grid(axis="x", alpha=0.55)
            plt.yticks(fontsize=14)
            plt.xticks(fontsize=16)
            plt.title(f"Word count of most frequent words\n in titles by group: {key}", fontsize=22)
            plt.ylabel("Most frequent words", fontsize=20)
            plt.xlabel("Count", fontsize=20)
            ax.invert_yaxis()
            for i, v in enumerate(df["count"]):
                ax.text(v + 0.05, i + .25, "Count: " + str(v), fontsize=15, color='dimgrey')
            plt.savefig(get_output_path("img", "analysis_grouped", f"most_common_title_words_by_groups_{key}.png"), dpi=300, orientation="landscape")

            # create wordcloud
            wordcloud = WordCloud(width=1600, height=800, background_color="white").generate(title_words_combined_by_group)
            plt.figure(figsize=(20,10))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.tight_layout(pad=0)
            wordcloud.to_file(get_output_path("img", "analysis_grouped", f"title_wordcloud_{key}.png"))
        except TypeError:
            pass

        most_frequent_by_groups = {
            key: most_common_by_groups_json
        }

        try:
            most_frequent_titles_by_groups = {
                key: most_common_title_words_by_groups_json
            }
        except TypeError:
            pass

        output = {
            key : {
                "number_of_articles": number_of_articles,
                "initial_number_of_words": number_of_words,
                "average_number_of_words_per_article": round(number_of_words/number_of_articles, 2),
                "number_of_words_after_filtering": number_of_remaining_words,
                "ratio_remaining_words_to_initial_number": round(number_of_remaining_words/number_of_words, 2)
            }
        }
        analysis_output_json.append(output)
        most_common_words_by_groups_json.append(most_frequent_by_groups)
        title_words_by_groups_json.append(most_frequent_titles_by_groups)


    # with open(get_output_path("json", "analysis_grouped", "grouped_statistics.json"), "w") as file:
    #     json.dump(analysis_output_json, file, indent=4)

    # with open(get_output_path("json", "analysis_grouped", "most_common_words_per_group.json"), "w") as file:
    #     json.dump(most_common_words_by_groups_json, file, indent=4)

    with open(get_output_path("json", "analysis_grouped", "most_common_title_words_by_group.json"), "w") as file:
        json.dump(title_words_by_groups_json, file, indent=4)

    # print("Analysis per group successful")


if __name__ == "__main__":
    # create_directory("img")
    # create_directory("json")
    # get_analysis()
    # get_analysis_over_all_articles()
    get_grouped_analysis()
