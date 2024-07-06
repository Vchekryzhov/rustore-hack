require 'uri'
class ParseImagesJob < ApplicationJob
  def perform(*)
    Image.all.each do |image|
      file = URI.open(image.rustore_link)
      image.image.attach(io: file  , filename: "some_image")
    rescue StandardError
      ''
    end
  end
end
