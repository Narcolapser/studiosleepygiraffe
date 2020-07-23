class BlogController < ApplicationController
	def index
		posts = []
		directories = Dir["/home/toben/Code/blog/*-*-*"]
		for directory in @directories
			@post = {}
			@post["date"] = directory[22..32]
			info = JSON.load File.open directory+"/info.json"
			#@post["info"] = info
			@post['title'] = info['title']
			#@post['content'] = directory+"/info.md"
			@post['cover'] = info['cover']
			@post['author'] = info['author']
			@posts.push @post
		end
		render :json => @posts
	end
	
	def show
		render :json => params[:id]
	end
end


# {"date"=>"2020-06-18", "info"=>{"content_file"=>"2020-06-04.md", "tags"=>["simple_systems socket"], "author"=>"Toben Archer", "cover"=>"sleepygiraffe7.jpg", "cover_text"=>"A sleepy giraffe", "date"=>"2020-06-04", "title"=>"Simple Systems Series Part 1: Sockets"}}
