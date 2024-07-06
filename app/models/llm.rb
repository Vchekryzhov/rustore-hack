require 'httparty'

class Llm
  include HTTParty
  default_timeout 5000

  def self.call(system_prompt:, user_prompt:)
    url = Prompt.first_or_create.llm_url
    raise 'Set LLM URL' if url.blank?
    response = post("#{url}/generate", body: {system_prompt: , query: user_prompt}.to_json, headers: { 'Content-Type' => 'application/json' })
    if response.success?
      response.parsed_response
    else
      { error: "Failed LLM: #{response.message}" }
    end
  end

end
