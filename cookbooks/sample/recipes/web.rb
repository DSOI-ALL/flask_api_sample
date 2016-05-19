%w{ python-pip python-dev screen }.each do |p|
	package p
end

bash "install-requirements" do
	cwd "#{node[:base_folder]}/webapp"
	code <<-EOH
		pip install -r requirements.txt
	EOH
	user "root"
	action :run
end

template "#{node[:base_folder]}/webapp/frontend_settings.cfg" do
	source "frontend_settings.cfg.erb"
	user "root"
	group "root"
end

template "/etc/init/frontend.conf" do
	source "frontend.conf.erb"
	user "root"
	group "root"
end

bash "start-flaskapi" do
	code <<-EOH
		service frontend restart
	EOH
	user "root"
	action :run
end