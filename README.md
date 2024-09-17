## Instruções

Para executar a expansão de consultas com os parâmetros utilizados no projeto atual, basta seguir as instruções abaixo:

1 - Na raiz do projeto executar **prepare_data.py** para obter os arquivos que serão usados. Os arquivos usados são:
	
    Vocabulary: 
    https://github.com/microsoft/MSMARCO-Passage-Ranking/tree/master/Baselines 

    Word vectors: 
    https://fasttext.cc/docs/en/english-vectors.html 

    MSMARCO queries and qrels: 
    https://ir-datasets.com/msmarco-passage.html#msmarco-passage/train/judged 
	

2 -  Copiar /flows/queries_expansion_config para a raiz do projeto e editar os seguintes parâmetros para que fiquem com o caminho dos arquivos baixados anteriormente:

        input:
            data_source: "data/queries_train_judged.csv"

        embedding:
            data_source: "data/wiki-news-300d-1M.vec"
            vocabulary: "data/word-vocab-small.csv"

        writer:
            cluwords_repr_path: "data_output/queries_train_judged_thresh_0.6.npz"
            data_path: "data_output/queries_train_judged_thresh_0.6.parquet"

3 - Para iniciar o processo, execute os comandos abaixo na raiz do projeto:

```
poetry shell
poetry install
python -m spacy download en
python run_cluwords_pipeline.py
```

As 161 queries com pelo menos 5 julgamentos demoram cerca de 25 minutos para serem expandidas usando as configurações acima.

## Referências

```
title={CluWords: Exploiting SemanticWord Clustering Representation for Enhanced Topic Modeling},
author={Viegas, Felipe and Canuto, Sérgio and Gomes, Christian and Luiz, Washington and Rosa, 
Thierson and Ribas, Sabir and Rocha, Leonardo and Gonçalves, Marcos André},
booktitle={The Twelfth ACM International Conference on Web Search and Data Mining (WSDM ’19)},
year={2019},
organization={ACM}
```

```
title={CluHTM - Semantic Hierarchical Topic Modeling based on CluWords},
author={Viegas, Felipe and Cunha, Washington and Gomes, Christian and  Pereira Antonio and Rocha, Leonardo and Gonçalves, Marcos André},
booktitle={The 58th Annual Meeting of the Association for Computational Linguistics (ACL ’20)},
year={2020},
organization={ACL}
```
