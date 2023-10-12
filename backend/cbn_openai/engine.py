from elastic_site_search import Client


client = Client(api_key="WcWWn5UPyiL-Vo8gR36y")

document_types = client.document_types("cbn-swifttype")
# print(document_types["body"])
document_type = client.document_type("cbn-swifttype", "entity-node")
# print(document_type)
documents = client.documents("cbn-swifttype", "entity-node")
# print(documents)
# print([document for document in documents["body"]])
# print(len(documents["body"]))
results = client.search("cbn-swifttype", "Pat Robertson", {"filters": {"entity-node": {"s_type": "article"}}})
print(results["body"]["records"]["entity-node"][0])
# "5c13d39f14cc8a79e9f4cea6" special_page
