from google.cloud import firestore

# The `project` parameter is optional and represents which project the client
# will act on behalf of. If not supplied, the client falls back to the default
# project inferred from the environment.
db = firestore.Client(project='mercurial-shape-387021')

groceries_ref = db.collection('Groceries')
docs = groceries_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')