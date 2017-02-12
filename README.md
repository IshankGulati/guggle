
# Guggle
A simple elasticsearch like search engine.

### Example

An api endpoint for indexing

```
POST /index
{
"id": "1",
"title": "quick fox",
"data": "A fox is usually quick and brown."
}

200 OK

POST /index
{
"id": "2",
"title": "lazy dog"
"data": "A quick brown fox jumped over lazy dog. A fox is always jumping."
}

200 OK
```

An api endpoint for search
```
GET /search?q=quick%20fox

[
{
    "id": "1",
    "title": "quick fox",
    "data": "A fox is usually quick and brown."
},
{
    "id": "2",
    "title": "lazy dog"
    "data": "A quick brown fox jumped over lazy dog. A fox is always jumping."
}]


GET /search?q=dog

[
{
    "id": "2",
    "title": "lazy dog"
    "data": "A quick brown fox jumped over lazy dog. A fox is always jumping."
}]


GET /search?q=quick%20dog

[
{
    "id": "2",
    "title": "lazy dog"
    "data": "A quick brown fox jumped over lazy dog. A fox is always jumping."
},
{
    "id": "1",
    "title": "quick fox",
    "data": "A fox is usually quick and brown."
}]

```
