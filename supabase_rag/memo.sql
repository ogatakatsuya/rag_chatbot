/* semantic searchをするための関数 */
CREATE FUNCTION search_full_texts(
    category_name TEXT,
    query halfvec
) 
RETURNS TABLE (
    id      integer,
    content TEXT,
    category_id integer,
    course_code varchar,
    similarity float
) 
LANGUAGE SQL STABLE
AS $$
    SELECT DISTINCT
        b.full_text_id, b.content, b.category_id, b.course_code, b.similarity
    FROM (
        SELECT  
            documents.full_text_id, 
            full_texts.content,
            full_texts.category_id,
            full_texts.course_code,
            documents.embedding <=>query as similarity
        FROM documents
        JOIN full_texts ON documents.full_text_id = full_texts.id
        JOIN categories ON full_texts.category_id = categories.id
        WHERE categories.name = category_name
        ORDER BY similarity
        LIMIT 15
    ) AS b
    ORDER BY b.similarity ASC;
$$;


create table categories (
  id integer primary key generated always as identity,
   name varchar(50)
  );

create table full_texts (
  id integer primary key generated always as identity, 
  content text not null,
  category_id integer not null,
  course_code varchar(10) not null unique,
  foreign key (category_id) references categories(id)
);

create type embed_type as enum('full_text', 'info_text', 'instructor_text', 'content_text');


create table documents (
  id integer primary key generated always as identity,
  embedding halfvec(1536),
  full_text_id integer not null,
  created_at timestamp with time zone default now(),
  type embed_type not null,
  foreign key (full_text_id) references full_texts(id)
    on delete cascade
);
