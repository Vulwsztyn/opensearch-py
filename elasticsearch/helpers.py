from itertools import islice

def bulk_index(client, docs, chunk_size=500, **kwargs):
    success, failed = [], []
    docs = iter(docs)
    while True:
        chunk = islice(docs, chunk_size)
        bulk_actions = []
        for d in chunk:
            action = {'index': {}}
            for key in ('_index', '_parent', '_percolate', '_routing',
                        '_timestamp', '_ttl', '_type', '_version',):
                if key in d:
                    action['index'][key] = d.pop(key)

            bulk_actions.append(action)
            bulk_actions.append(d.get('_source', d))

        if not bulk_actions:
            return success, failed

        resp = client.bulk(bulk_actions, **kwargs)

        for item in resp['items']:
            if item['create']['ok']:
                success.append(item)
            else:
                failed.append(item)
