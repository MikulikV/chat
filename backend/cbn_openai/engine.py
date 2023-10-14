from elastic_site_search import Client
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    client = Client(api_key=os.environ["SEARCH_API_KEY"])

    document_types = client.document_types("cbn-swifttype")
    print(document_types["body"])
    document_type = client.document_type("cbn-swifttype", "entity-node")
    print(document_type)
    documents = client.documents("cbn-swifttype", "entity-node")
    print(documents)
    print([document for document in documents["body"]])
    print(len(documents["body"]))
    results = client.search("cbn-swifttype", "Pat Robertson", {"filters": {"entity-node": {"s_type": "article"}}})
    print(results["body"]["records"]["entity-node"][0])
