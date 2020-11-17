class FeedController < ApplicationController
	def index
		posts = []
		directories = Dir['/home/toben/Code/blog/*-*-*']
		for directory in directories
			post = {}
			info = JSON.load(File.open("#{directory}/info.json"))
			post['title'] = info['title']
			post['link'] = "http://www.studiosleepygiraffe.com/blog/posts/#{directory[22..32]}"
			post['date'] = Date.strptime(directory[22..32], '%Y-%m-%d')
			post['author'] = info['author']
			
			markdown = File.open("#{directory}/post.md")
			content = markdown.read
			lines = content.split("\n")
			
			post['text'] = lines.slice(0,3).join("\n")

			posts.push post
		end
		
		directories = Dir['/home/toben/Code/ssg/*']
		for directory in directories
			if File.exist?(directory+'/info.json')
				logs = JSON.load File.open directory+'/logs.json'
				for log in logs['posts']
					post = {}
					post['title'] = "#{directory[21..-1].capitalize()}: #{log['title']}"
					post['link'] = "http://www.studiosleepygiraffe.com/logs/#{directory[21..-1]}"
					post['date'] = Date.strptime(log['date'], '%Y-%m-%d')
					post['text'] = log['message']
					post['author'] = log['author']
					posts.push post
				end
			end
		end
		
		posts = posts.sort { |a,b| b['date'] <=> a['date'] }
		for post in posts
			post['date'] = post['date'].strftime('%a, %d %b %Y 00:00:00 GMT')
		end
		if params[:ext] == 'rss'
			render template: "feed/feed.html.erb", :locals => { :posts => posts.slice(0,20) }, :layout => false
		else
			render json: posts.slice(0,20)
		end
	end
end
