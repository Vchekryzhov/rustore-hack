class ParseChunksCsvJob < ApplicationJob
  def perform(*)
    csv = CSV.read('public/chunks.csv')
    header = csv.shift
    csv.each do |line|
      Chunk.create(content: line[header.index("Content_Chunk")], article_id: line[header.index('Id')])
    end
  end
end