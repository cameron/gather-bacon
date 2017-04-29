# missing features

## blockers
- python 3
- concurrency: gevent instead of greenhouse

## important
- relationships
  - bulk creation
  - remove 
- name  
  - uniq_to_parent prefix search (searching through your own contact book, eg)
- setting a nonexistent flag doens't fail 

## nice to have
- relationships
  - lookup relationships with WHERE flags clause for awesome filtering
  - traverse relationships without fetching node
    - eg, user -> groups of friends w/friend nodes (not necessary to grab group nodes)
- props
  - bulk fetch
- child->parent api (only parent->child)
- cardinality
- value field
- jsonification
  - flags -> json attrs
  - fetched attrs -> json attrs
- string name -> class hash for user classes on the databacon module
  - eg, for making a generic url id -> instance converter
- encode permissions in id (not sure if this needs to be part of databacon or not)

# annoying
- <attr>.flags is referencable but not part of the public API (.flag is correct)
- rename the dh object/kwarg to row