class LlmJob < ApplicationJob

  def perform(message)
    context = SemanticSearch.new.perform(message.text).map(&:search_index).join(" ")
    message.update(context: )
    system_prompt = Prompt.first_or_create.system
    user_prompt = Prompt.first_or_create.user % { context:, query: message.text }
    text = Llm.call(system_prompt: , user_prompt: )
    Message.create(text: , room_id: message.room_id, user: User.find_or_create_by(name: "admin"))
  end



end