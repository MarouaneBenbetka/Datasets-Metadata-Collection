import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string


def generate_tags(title: str):

    clean_title = title.translate(
        str.maketrans('', '', string.punctuation)).lower()

    # Step 2: Tokenize the title
    tokens = word_tokenize(clean_title)

    # Step 3: Remove stop words
    stop_words = set(stopwords.words('english') +
                     ["dataset", "data", "datasets"])
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Step 4: The remaining words can be used as tags
    tags = filtered_tokens

    return tags
