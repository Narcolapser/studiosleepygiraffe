class PostsController < ApplicationController
	def index
		posts = []
		directories = Dir['/home/toben/Code/blog/*-*-*']
		for directory in directories
			post = {}
			post['date'] = directory[22..32]
			post['url'] = '/posts/' + directory[22..32]
			info = JSON.load(File.open("#{directory}/info.json"))
			post['title'] = info['title']
			post['cover'] = info['cover']
			post['author'] = info['author']
			
			posts.push post
		end
		render json: posts
	end
	
	def show
		directories = Dir['/home/toben/Code/blog/*-*-*']
		posts = directories.map {|dir| dir[22..32]}
		if posts.include? params[:id]
			info = JSON.load File.open '/home/toben/Code/blog/' + params[:id] + '/info.json'
			render :json => info
		else
			render json: {'Status':'Failure'}
		end
	end
end
