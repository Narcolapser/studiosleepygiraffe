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
			post['cover'] = 'cover.jpg'
			post['author'] = info['author']
			
			posts.push post
		end
		posts = posts.sort { |a,b| b['date'] <=> a['date'] }
		render json: posts
	end
	
	def show
		directories = Dir['/home/toben/Code/blog/*-*-*']
		posts = directories.map {|dir| dir[22..32]}
		if posts.include? params[:id]
			info = JSON.load File.open '/home/toben/Code/blog/' + params[:id] + '/info.json'
			info['date'] = params[:id]
			render :json => info
		else
			render json: {'Status':'Failure'}
		end
	end
	
	def resources
		directories = Dir['/home/toben/Code/blog/*-*-*']
		posts = directories.map {|dir| dir[22..32]}
		if posts.include? params[:id]
			resource = params[:resource] + '.' + params[:ext] 
			if resource == 'post.md'
				# return the mark down
				postmd = File.open '/home/toben/Code/blog/' + params[:id] + '/post.md'
				render plain: postmd.read
			elsif resource  == 'cover.jpg'
				# return the cover image
				render file: '/home/toben/Code/blog/' + params[:id] + '/cover.jpg', layout: false
			else
				info = JSON.load File.open '/home/toben/Code/blog/' + params[:id] + '/info.json'
				files = info['files']
				
				if files.include? resource
					# return the resource
					render file: '/home/toben/Code/blog/' + params[:id] + '/' + resource, layout: false
				else
					render(:file => File.join(Rails.root, 'public/404.html'), :status => 404, :layout => false)
#					render json: {'Status':'Failure'}
#					return File.open '/home/toben/Code/blog/' + params[:id] + '/post.md'
#					return render(:file => File.join(Rails.root, 'public/404.html'), :status => 404, :layout => false)
				end
			end
		end
	end
end
