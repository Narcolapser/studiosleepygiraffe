class FeedController < ApplicationController
	def index
		posts = []
		directories = Dir['/home/toben/Code/blog/*-*-*']
		for directory in directories
			post = {}
			info = JSON.load(File.open("#{directory}/info.json"))
			post['title'] = info['title']
			post['link'] = "http://www.studiosleepygiraffe.com/blog/posts/#{directory[22..32]}"
			post['date'] = directory[22..32]
			post['author'] = info['author']
			
			markdown = File.open("#{directory}/post.md")
			content = markdown.read
			lines = content.split('\n')
			
			post['text'] = lines.slice(0,3).join('\n')

			posts.push post
		end
		
		directories = Dir['/home/toben/Code/ssg/*']
		for directory in directories
			if File.exist?(directory+'/info.json')
				logs = JSON.load File.open directory+'/logs.json'
				for log in logs['posts']
					post = {}
					post['title'] = "#{directory.capitalize()}: #{log['title']}"
					post['link'] = "http://www.studiosleepygiraffe.com/logs/#{directory}"
					post['date'] = log['date']
					post['text'] = log['message']
					post['author'] = log['author']
					post['log'] = log
					posts.push post
				end
			end
		end
		
		posts = posts.sort { |a,b| b['date'] <=> a['date'] }
		if params[:ext] == 'rss'
			render template: "feed" # , content_type: "application/rss"
		else
			render json: posts.slice(0,20)
		end
	end
end
