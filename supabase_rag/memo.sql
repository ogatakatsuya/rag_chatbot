/* semantic searchをするための関数 */
CREATE FUNCTION search_full_texts(
    category_name TEXT,
    embedding VECTOR
) 
RETURNS TABLE (
    content TEXT
) 
LANGUAGE SQL STABLE
AS $$
    SELECT 
        full_texts.content
    FROM documents
    JOIN categories ON documents.category_id = categories.id
    JOIN full_texts ON documents.full_text_id = full_texts.id
    WHERE categories.name = category_name
    ORDER BY documents.embedding <-> embedding
    LIMIT 5;
$$;
