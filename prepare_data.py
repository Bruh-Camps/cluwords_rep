import os
import zipfile
import pandas as pd
import urllib.request
import ir_datasets

vocab_path = "data/word-vocab-small.csv"
embedding_path = "data/wiki-news-300d-1M.vec"
queries_path = "data/queries_train_judged.csv"


#Website for vocab: https://github.com/microsoft/MSMARCO-Passage-Ranking/tree/master/Baselines
if not os.path.isfile(vocab_path):
    url = "https://raw.githubusercontent.com/microsoft/MSMARCO-Passage-Ranking/master/Baselines/data/word-vocab-small.tsv"
    print("Baixando vocabulário ...")
    df = pd.read_csv(url, sep='\t').iloc[:, 0]
    df.to_csv(vocab_path, index=False)
    print("Vocabulário salvo!")

#Vectors website: https://fasttext.cc/docs/en/english-vectors.html
if not os.path.isfile(embedding_path):
    url = "https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip"
    print("Baixando embedding ... (pode demorar)")
    urllib.request.urlretrieve(url, embedding_path)
    with zipfile.ZipFile(embedding_path, 'r') as zip_ref:
        zip_ref.extractall("/data")
    os.remove(embedding_path)
    print("Embedding salvo!")

# queries and qrels website: https://ir-datasets.com/msmarco-passage.html#msmarco-passage/train/judged
if not os.path.isfile(queries_path):
    dataset = ir_datasets.load("msmarco-passage/train/judged") #"msmarco-passage/dev/judged"
    
    # ------------------- SALVA OS QRELS EM UM DATAFRAME ------------------------
    qrels = []
    for qrel in dataset.qrels_iter():
        qrel # namedtuple<query_id, doc_id, relevance, iteration>
        qrels.append({
            'query_id': qrel.query_id,
            'doc_id': qrel.doc_id,
            'relevance': qrel.relevance
        })
    qrels_df = pd.DataFrame(qrels)

    # ------------------- CONTA O NUM. DE JULGAMENTOS POR QUERY ------------------------
    relevant_docs = qrels_df[qrels_df['relevance'] > 0]
    relevant_counts = relevant_docs.groupby('query_id').size().reset_index(name="relevant_count")

    # ------------------- SALVA AS QUERIES EM UM DATAFRAME ------------------------
    queries = []
    for query in dataset.queries_iter():
        queries.append({
            'query_id': query.query_id,
            'text': query.text
        })
    queries_df = pd.DataFrame(queries)

    # ------------------- FILTRA QUERIES QUE POSSUAM AO MENOS 5 JULGAMENTOS ------------------------
    queries_df = queries_df.merge(relevant_counts, left_on='query_id', right_on='query_id', how='inner')
    filtered_df = queries_df[queries_df['relevant_count'] >= 5]
    print(f"Das {len(queries_df)} queries baixadas, {len(filtered_df)} delas foram salvas por ter pelo menos 5 julgamentos.")

    filtered_df[["query_id","text"]].to_csv(queries_path, header=True, index=False)
