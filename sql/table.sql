CREATE TABLE documents (
    id UUID PRIMARY KEY,
    title text not null,
    tag text not null,
    categories text not null,
    description text not null,
    embedding vector(1536)
);
