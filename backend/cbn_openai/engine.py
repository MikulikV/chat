from elastic_site_search import Client


client = Client(api_key="WcWWn5UPyiL-Vo8gR36y")

document_types = client.document_types("cbn-swifttype")
print(document_types["body"])
document_type = client.document_type("cbn-swifttype", "63c5525f7a9df8ff160c785a")
print(document_type)
documents = client.documents("cbn-swifttype", "63c5525f7a9df8ff160c785a")
# print(documents)
print([document for document in documents["body"] if document["s_type"] == "video"])
# "5c13d39f14cc8a79e9f4cea6" special_page
