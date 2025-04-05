/* semantic searchをするための関数 */
CREATE FUNCTION search_full_texts(
    category_name TEXT,
    query halfvec
) 
RETURNS TABLE (
    id      integer,
    content TEXT,
    similarity float
) 
LANGUAGE SQL STABLE
AS $$
    SELECT DISTINCT
        b.full_text_id, b.content, b.similarity
    FROM (
        SELECT  
            documents.full_text_id, 
            full_texts.content,
            documents.embedding <=>query as similarity
        FROM documents
        JOIN categories ON documents.category_id = categories.id
        JOIN full_texts ON documents.full_text_id = full_texts.id
        WHERE categories.name = category_name
        ORDER BY similarity
        LIMIT 15
    ) AS b
    ORDER BY b.similarity ASC;
$$;