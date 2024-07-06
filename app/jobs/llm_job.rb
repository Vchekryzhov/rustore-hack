class LlmJob < ApplicationJob
  queue_with_priority 2
  def perform(message)
    chunks = SemanticSearch.new.perform(message.text, :chunks)[0..3]
    context = build_context(chunks)

    message.update(context: context )
    config = Config.first_or_create
    system_prompt = config.system
    user_prompt = config.user % { context:, query: message.text }

    text = if config.llm_enabled
             llm_response = Llm.call(system_prompt: , user_prompt: )
             if llm_response[:success]
                      llm_response[:message]
                    else
                      build_fallback_response(chunks)
                    end
           else
             build_fallback_response(chunks)
           end


    Message.create(text: , room_id: message.room_id, user: User.find_or_create_by(name: "admin"), references: build_references(chunks), context: "#{system_prompt} \n\n\n\n #{user_prompt}"  )
  end
  def build_context(chunks)

    chunks.map do |chunk|
      article = chunk.article
      <<-TEXT.strip_heredoc
Заголовок: #{article&.name}
Ссылка: #{article&.link}
Текст: #{chunk.search_index}
      TEXT
    end.join("\n\n\n-------------------------------------------------------------------------------------------------------\n\n\n")
  end

  def build_references(chunks)
    Article.where(id: chunks.map(&:article_id).uniq[0..5]).map do |article|
      {
        name: article.name,
        url: article.link
      }.to_json
    end
  end
  def build_fallback_response(chunks)
    chunks[0..5].map do |chunk|
      article = chunk.article
      next if article.nil?
      <<-TEXT.strip_heredoc
        1. [#{article.summary}](#{article.link})
      TEXT
    end.compact.join("\n\n")
  end
end