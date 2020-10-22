class ProjectsController < ApplicationController
	def index
		posts = Array.new
		directories = Dir['/home/toben/Code/ssg/*']
		for directory in directories
			print directory
			if File.exist?(directory+'/info.json')
				info = JSON.load File.open directory+'/info.json'
				info['url'] = '/projects' + info['url']
				posts.push info
			end
		end
		posts = posts.sort { |a,b| a['rank'] <=> b['rank'] }
		render json: posts
	end
	
	def show
		directories = Dir['/home/toben/Code/ssg/*']
		posts = directories.map {|dir| dir[21..dir.length]}
		print(posts)
		if posts.include? params[:id]
			info = JSON.load File.open '/home/toben/Code/ssg/' + params[:id] + '/info.json'
			render :json => info
		else
			render json: {'Status':'Failure'}
		end
	end

	def resources
		directories = Dir['/home/toben/Code/ssg/*']
		posts = directories.map {|dir| dir[21..dir.length]}
		if posts.include? params[:id]
			resource = params[:resource] + '.' + params[:ext] 
			if resource == 'README.md'
				# return the mark down
				postmd = File.open '/home/toben/Code/ssg/' + params[:id] + '/README.md'
				render plain: postmd.read
			elsif resource  == 'banner1.png'
				# return the the first banner image
				render file: '/home/toben/Code/ssg/' + params[:id] + '/banner1.png', layout: false
			elsif resource  == 'banner2.png'
				# return the the first banner image
				render file: '/home/toben/Code/ssg/' + params[:id] + '/banner2.png', layout: false
			else
				info = JSON.load File.open '/home/toben/Code/ssg/' + params[:id] + '/info.json'
				files = info['files']
				
				if files.include? resource
					# return the resource
					render file: '/home/toben/Code/ssg/' + params[:id] + '/' + resource, layout: false
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
