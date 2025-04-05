/* semantic searchをするための関数 */
CREATE FUNCTION search_full_texts(
    category_name TEXT,
    query halfvec
) 
RETURNS TABLE (
    id      integer,
    content TEXT
) 
LANGUAGE SQL STABLE
AS $$
    SELECT
        documents.id, full_texts.content
    FROM documents
    join categories on documents.category_id = categories.id
    join full_texts on documents.full_text_id = full_texts.id
    where categories.name = category_name
    ORDER BY documents.embedding <=> query ASC
    LIMIT 5;
$$;