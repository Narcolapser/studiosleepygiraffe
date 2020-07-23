module Blog
	class PostsController < ApplicationController

		def index
			render :json => {'test' => 'works'}
		end

		def show
			render :json => params[:id]
		end
	end
end
