# coding=utf-8
"""
Logs repository.
"""
from elasticsearch import Elasticsearch

from src.constants import CTX_TESTING, DEFAULT_LIMIT
from src.use_case.interface.logs_repository import LogsRepository, LogFetchError
from src.util.mac import get_mac_variations


class ElasticSearchRepository(LogsRepository):
    """
    Interface to the log repository.
    """

    def __init__(self, configuration):
        self.config = configuration

    def get_logs(self, ctx, limit=DEFAULT_LIMIT, username=None, devices=None):
        """
        Get the logs related to the username and to the devices.
        :param ctx:  context
        :param username:  username
        :param devices:  MAC addresses of the devices
        :param limit: limit result
        :return: logs
        """
        if not self.config.ELK_HOSTS:
            raise LogFetchError('no elk host configured')

        if ctx.get(CTX_TESTING):  # Do not actually query elasticsearch if testing...
            return ["test_log"]

        # Prepare the elasticsearch query...
        query = {
            "sort": {
                '@timestamp': 'desc',  # Sort by time
            },
            "query": {
                "bool": {
                    "should": [  # "should" in a "bool" query basically act as a "OR"
                        {"match": {"message": username}},  # Match every log mentioning this member
                        # rules to match MACs addresses are added in the next chunk of code
                    ],
                    "minimum_should_match": 1,
                },
            },
            "_source": ["@   timestamp", "message"],  # discard any other field than timestamp & message
            "size": limit,
        }

        # Add the macs to the "should"
        for addr in devices:
            variations = map(
                lambda x: {"match_phrase": {"message": x}},
                get_mac_variations(addr)
            )
            # noinspection PyTypeChecker
            query["query"]["bool"]["should"] += list(variations)

        # TODO: instantiate only once the Elasticsearch client
        es = Elasticsearch(self.config.ELK_HOSTS)
        res = es.search(index="", body=query)['hits']['hits']

        return list(map(
            lambda x: "{} {}".format(x["_source"]["@timestamp"], x["_source"]["message"]),
            res
        ))
