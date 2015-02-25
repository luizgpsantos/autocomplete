# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse

from elasticsearch import Elasticsearch


def main():
    parser = argparse.ArgumentParser(description='Create suggestions.')
    parser.add_argument('-e', '--elasticsearch', required=True, help="Elasticsearch URL")
    args = parser.parse_args()

    es_busca = Elasticsearch(hosts=[args.elasticsearch])
    es_local = Elasticsearch()

    results = es_busca.search(index=".measure-buscapadrao*", search_type="count", body={
        "aggs": {
            "search_terms": {
                "terms": {
                    "field": "search_term_original.raw",
                    "size": 5000
                }
            }
        }
    })

    es_local.indices.create(index="search_terms")
    es_local.indices.put_mapping(index="search_terms", doc_type="search_terms", body={
        "search_terms": {
            "properties": {
                "suggest": {
                    "type": "completion",
                    "index_analyzer": "simple",
                    "search_analyzer": "simple",
                    "payloads": True
                }
            }
        }
    })

    for result in results["aggregations"]["search_terms"]["buckets"]:
        es_local.index(index="search_terms", doc_type="search_terms", body={
            "suggest": {
                "input": result["key"],
                "weight": result["doc_count"]
            }
        })

if __name__ == '__main__':
    main()
