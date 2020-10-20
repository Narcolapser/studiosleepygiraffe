class LogsController < ApplicationController
	def index
		posts = Array.new
		directories = Dir['/home/toben/Code/ssg/*']
		for directory in directories
			print directory
			if File.exist?(directory+'/info.json')
				info = JSON.load File.open directory+'/info.json'
				info['url'] = '/logs' + info['url']
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
			info = JSON.load File.open '/home/toben/Code/ssg/' + params[:id] + '/logs.json'
			render json: info
		else
			render json: {'Status':'Failure'}
		end
	end
end


