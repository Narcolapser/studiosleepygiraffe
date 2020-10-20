require 'set'

class TagsController < ApplicationController
	def index
		tags = Set.new
		directories = Dir['/home/toben/Code/blog/*-*-*']
		for directory in directories
			info = JSON.load(File.open("#{directory}/info.json"))
			for tag in info['tags']
				tags.add(tag)
			end
		end
		render json: tags
	end
	
	def tag
		directories = Dir['/home/toben/Code/blog/*-*-*']
		posts = []
		for directory in directories
			info = JSON.load(File.open("#{directory}/info.json"))
			match = false
			for tag in info['tags']
				if tag.downcase == params[:tag].downcase
					match = true
					break
				end
			end
			if match
				info['date'] = directory[22..32]
				posts.push info
			end
		end
		render json: posts
	end
end
