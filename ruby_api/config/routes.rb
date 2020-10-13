Rails.application.routes.draw do
	get 'welcome/index'
	get 'blog/index'
	get 'blog', to: 'blog#index'
	get 'blog/posts/index'
	
	get 'posts', to: 'posts#index'
	
	get 'posts/:id/:resource', to: 'posts#resources'
	
	#get 'blog/posts/:id', to 'blog/posts#show'
#	get 'blog/post/index'

	# For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
	resources :posts
	resources :logs
	resources :projects
	resources :tags
	
	
	root 'welcome#index'
end
