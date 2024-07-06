class LlmJob < ApplicationJob

  def perform(message)
    context = build_context(message)

    message.update(context: context[0..10000] )
    system_prompt = Prompt.first_or_create.system
    user_prompt = Prompt.first_or_create.user % { context:, query: message.text }
    text = Llm.call(system_prompt: , user_prompt: )
    Message.create(text: , room_id: message.room_id, user: User.find_or_create_by(name: "admin"))
  end
  def build_context(message)
    SemanticSearch.new.perform(message.text).map do |article|
      <<-TEXT.strip_heredoc
Заголовок: #{article.name}
Ссылка: #{article.link}
Текст: #{article.search_index}
      TEXT
    end.join("------------------------------\n")
  end
end