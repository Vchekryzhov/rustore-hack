class SemanticSearch
  def perform(query)
    sql = <<-SQL
      WITH articles_semantic_search AS (
          SELECT id, RANK () OVER (ORDER BY embedding <=> :embedding) AS rank
          FROM #{Article.quoted_table_name}
          ORDER BY embedding <=> :embedding
          LIMIT 100
      ),
      articles_keyword_search AS (
          SELECT id, RANK () OVER (ORDER BY ts_rank_cd(to_tsvector('english', search_index), query) DESC) AS rank
          FROM #{Article.quoted_table_name}, plainto_tsquery('english', :query) query
          WHERE to_tsvector('english', search_index) @@ query
          ORDER BY ts_rank_cd(to_tsvector('english', search_index), query) DESC
          LIMIT 100
      ),
      images_semantic_search AS (
          SELECT id, article_id, RANK () OVER (ORDER BY embedding <=> :embedding) AS rank
          FROM #{Image.quoted_table_name}
          ORDER BY embedding <=> :embedding
          LIMIT 100
      ),
      images_keyword_search AS (
          SELECT id, article_id, RANK () OVER (ORDER BY ts_rank_cd(to_tsvector('english', search_index), query) DESC) AS rank
          FROM #{Image.quoted_table_name}, plainto_tsquery('english', :query) query
          WHERE to_tsvector('english', search_index) @@ query
          ORDER BY ts_rank_cd(to_tsvector('english', search_index), query) DESC
          LIMIT 100
      ),
      combined_search as (SELECT
          COALESCE(articles_semantic_search.id, articles_keyword_search.id, images_semantic_search.article_id, images_keyword_search.article_id ) AS id,
          COALESCE(images_semantic_search.id, images_keyword_search.id ) AS images_id,
          COALESCE(1.0 / (:article_weight + articles_semantic_search.rank), 0.0) as articles_semantic_rank,
          COALESCE(1.0 / (:article_weight + articles_keyword_search.rank), 0.0) as articles_keyword_rank,
          COALESCE(1.0 / (:image_weight + images_semantic_search.rank), 0.0) as images_semantic_rank,
          COALESCE(1.0 / (:image_weight + images_keyword_search.rank), 0.0) as images_keyword_rank
      FROM articles_semantic_search
      FULL OUTER JOIN articles_keyword_search ON articles_semantic_search.id = articles_keyword_search.id
      FULL OUTER JOIN images_semantic_search ON articles_semantic_search.id = images_semantic_search.article_id
      FULL OUTER JOIN images_keyword_search ON articles_semantic_search.id = images_keyword_search.article_id
  ),
    ranked_combined_search AS (
        SELECT DISTINCT ON (id) 
            id,
            images_id,
            articles_semantic_rank + articles_keyword_rank + images_semantic_rank + images_keyword_rank as score,
            articles_semantic_rank,
            articles_keyword_rank,
            images_semantic_rank,
            images_keyword_rank
        FROM combined_search
        ORDER by id, score desc
    )
    SELECT 
        ranked_combined_search.id,
        articles.name as name,
        CONCAT( articles.search_index,' ' , images.search_index ) as search_index,
        articles.link as link,
        score,
        articles_semantic_rank,
        articles_keyword_rank,
        images_semantic_rank,
        images_keyword_rank
    FROM ranked_combined_search
    LEFT JOIN articles on articles.id = ranked_combined_search.id
    LEFT JOIN images on images.id = ranked_combined_search.images_id
    ORDER BY score DESC
    LIMIT 20;
    SQL

    return [] if query.blank?
    Article.find_by_sql([sql, { embedding: TextEncoder.call(query).to_s, query:, article_weight: 1, image_weight: 1 }])
  end
end