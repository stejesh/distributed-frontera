========
Glossary
========


.. glossary::
    spider log
        A stream of encoded messages from spiders. Each message is product of extraction from document content. Most of
        the time it is links, scores, classification results.

    scoring log
        Contains score updating events and scheduling flag (if link needs to be scheduled for download) going from
        strategy worker to db worker.

    strategy worker
        Special type of worker, running the crawling strategy code: scoring the links, deciding if link needs to be
        scheduled (consults :term:`state cache`) and when to stop crawling. That type of worker is sharded.

    state cache
        In-memory data structure containing information about state of documents, whatever they were scheduled or not.
        Periodically synchronized with HBase.