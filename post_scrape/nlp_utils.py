import numpy as np
import pandas as pd
import spacy
from tqdm import tqdm
from constants import(
    DESC_K,
    ESRB_K,
    TITLE_K,
)

NORMED_DESC_K = f'normalized_{DESC_K}'

nlp = spacy.load('en_core_web_lg')  # lg has best word vectors


def normalize_text(s):
    """Lower, lemmatize, & drop filler tokens in s."""
    clean_tokens = []
    raw_tokens = nlp(s)
    for raw_token in raw_tokens:
        if raw_token.is_bracket:
            continue
        elif raw_token.is_currency:
            continue
        elif raw_token.is_punct:
            continue
        elif raw_token.is_space:
            continue
        elif raw_token.is_stop:
            continue
        else:
            clean_token = raw_token.lemma_.lower()
            clean_tokens.append(clean_token)

    norm_s = ' '.join(clean_tokens)
    return norm_s


def model_fit_transform(
    corpus,
    doc_term_vectorizer,
    model,
):
    """Apply doc_term_vectorizer to corpus for a doc-term matrix to fit model to."""
    doc_term_matrix = doc_term_vectorizer.fit_transform(corpus)
    words = doc_term_vectorizer.get_feature_names_out()
    topics_docs_matrix = model.fit_transform(doc_term_matrix).T
    topics_words_matrix = model.components_

    return topics_docs_matrix, topics_words_matrix, words


def latent_features(
    docs,
    top_n,
    topics_docs_matrix,
    topics_words_matrix,
    words,
):
    """Get the top_n words & documents per topic."""
    ds = []
    for i, (topic_docs_vector, topic_words_vector) in enumerate(zip(topics_docs_matrix, topics_words_matrix)):
        topic_top_docs_idxs = topic_docs_vector.argsort()[-top_n:][::-1]
        topic_top_docs = docs.iloc[topic_top_docs_idxs].values
        topic_top_docs = '\n'.join(topic_top_docs)
        
        topic_top_words_idxs = topic_words_vector.argsort()[-top_n:][::-1]
        topic_top_words = words[topic_top_words_idxs]
        topic_top_words = '\n'.join(topic_top_words)

        ds.append(
            {
                'latent_topic': i,
                'most_relevant_games': topic_top_docs,
                'most_relevant_words': topic_top_words,
            }
        )
    df = pd.DataFrame(ds)
    return df


def topic_model_breakdown(
    corpus,
    doc_term_vectorizer,
    docs,
    model,
    top_n,
):
    """Perform topic modeling of model (technique) on doc_term_vectorizer resultant (doc-term matrix)."""
    topics_docs_matrix, topics_words_matrix, words = model_fit_transform(corpus, doc_term_vectorizer, model)
    topics_df = latent_features(docs, top_n, topics_docs_matrix, topics_words_matrix, words)
    return topics_df


def topic_model_breakdown_per_esrb(
    data_df,
    doc_term_vectorizer,
    model,
    top_n,
):
    """Perform topic modeling of model on doc_term_vectorizer resultant (doc-term matrix) per ESRB rating."""
    dfs = []
    for esrb, group_df in data_df.groupby(ESRB_K):
        corpus = group_df[NORMED_DESC_K]
        docs = group_df[TITLE_K]
        
        topics_docs_matrix, topics_words_matrix, words = model_fit_transform(corpus, doc_term_vectorizer, model)
        topics_df = latent_features(docs, top_n, topics_docs_matrix, topics_words_matrix, words)
        topics_df[ESRB_K] = esrb
        
        dfs.append(topics_df)

    esrb_grouped_topics_df = pd.concat(dfs)
    esrb_grouped_topics_df.reset_index(inplace=True)
    return esrb_grouped_topics_df


def evaluate_model(selector, model, xs, ys):
    """Get results of cross validating model a la selector.split(xs, ys)."""
    preds = []
    truths = []
    for train_idxs, val_idxs in tqdm(selector.split(xs, ys)):
        kth_train_xs = xs[train_idxs]
        kth_train_ys = ys.iloc[train_idxs]
        kth_val_xs = xs[val_idxs]
        kth_val_ys = ys.iloc[val_idxs]

        model.fit(kth_train_xs, kth_train_ys)
        kth_pred_ys = model.predict(kth_val_xs)

        preds.append(kth_pred_ys)
        truths.append(kth_val_ys)

    preds = np.concatenate(preds).flatten()
    truths = np.concatenate(truths).flatten()

    return truths, preds
