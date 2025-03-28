from rag.client import client
#デバッグ用

collection_list = client.collections.list_all()

for collection in collection_list:
    print(collection)
collection_name = "class_data_full_text"

collection = client.collections.get(collection_name)

response = collection.aggregate.over_all(total_count=True)

print(f"Total objects in collection '{collection_name}': {response.total_count}")

# クライアントを閉じる
client.close()