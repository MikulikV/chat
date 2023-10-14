from langchain.docstore.document import Document
import re

# functions to prepare the data
def fix_newlines(text):
    return re.sub(r"(?<!\n)\n(?!\n)", " ", text)


def fix_tabs(text):
    return re.sub(r"(?<!\t)\t(?!\t)", " ", re.sub(r"\t{2,}", " \t ", text))


def remove_multiple_newlines(text):
    return re.sub(r"\n{2,}", " \n ", text)


def remove_multiple_spaces(text):
    return re.sub(r" +", " ", text)


def remove_time_codes(text):
    return re.sub(r"\d{2}:\d{2}:\d{2}", "", text)


def remove_stars_from_text(text):
    return text.replace("*", "")


def clean_text(data):
    cleaning_functions = [
        fix_tabs,
        remove_time_codes,
        remove_stars_from_text,
        fix_newlines,
        remove_multiple_newlines,
        remove_multiple_spaces,
    ]
    if isinstance(data, str):
        for cleaning_function in cleaning_functions:
            data = cleaning_function(data)
        prepared_data = data
    elif isinstance(data, list):
        prepared_data = []
        for document in data:
            for cleaning_function in cleaning_functions:
                document.page_content = cleaning_function(document.page_content)
            doc = Document(
                page_content=document.page_content,
                metadata=document.metadata
            )
            prepared_data.append(doc)
    
    return prepared_data