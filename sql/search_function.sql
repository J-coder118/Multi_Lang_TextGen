
create index on documents using ivfflat (embedding vector_cosine_ops)
with
  (lists = 100);
-- Create a function to search for documents
create function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int 
) returns table (
  title text,
  tag text,
  categories text,
  description text,
  similarity float
)
language sql stable
as $$
  select
    title,
    tag,
    categories,
    description,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where 1 - (documents.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
$$;