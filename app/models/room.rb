class Room < ApplicationRecord
  has_many :messages
  has_many :users, through: :messages

  def name
    "Комната #{id}"
  end

  after_create_commit -> (room) {RoomRelayJob.perform_later(room)}
end
