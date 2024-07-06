class LlmJob < ApplicationJob

  def perform(message)
    articles = SemanticSearch.new.perform(message.text)
    context = build_context(articles)

    message.update(context: context[0..10000] )
    config = Config.first_or_create
    system_prompt = config.system
    user_prompt = config.user % { context:, query: message.text }
    text = if config.llm_enabled
             llm_response = Llm.call(system_prompt: , user_prompt: )
             if llm_response[:success]
                      llm_response[:message]
                    else
                      build_fallback_response(articles)
                    end
           else
             build_fallback_response(articles)
           end


    Message.create(text: , room_id: message.room_id, user: User.find_or_create_by(name: "admin"))
  end
  def build_context(articles)
    articles.map do |article|
      <<-TEXT.strip_heredoc
Заголовок: #{article.name}
Ссылка: #{article.link}
Текст: #{article.search_index}
      TEXT
    end.join("------------------------------\n")
  end
  def build_fallback_response(articles)
    articles[0..5].map do |article|
      <<-TEXT.strip_heredoc
        1. [#{article.summary}](#{article.link})
      TEXT
    end.join("\n\n")
  end
end