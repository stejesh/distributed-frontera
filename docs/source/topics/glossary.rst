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