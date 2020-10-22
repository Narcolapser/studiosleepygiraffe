Rails.application.routes.draw do
	get 'welcome/index'
	get 'blog/index'
	get 'blog', to: 'blog#index'
	get 'blog/posts/index'
	
	get 'posts', to: 'posts#index'
	
	get 'posts/tags', to: 'tags#index'
	get 'posts/tags/:tag', to: 'tags#tag'
	get 'posts/:id/:resource.:ext', to: 'posts#resources'
	
	get 'projects/:id/:resource.:ext', to: 'projects#resources'
	
	#get 'blog/posts/:id', to 'blog/posts#show'
#	get 'blog/post/index'

	# For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
	resources :posts
	resources :logs
	resources :projects
	resources :tags
	
	
	root 'welcome#index'
end
