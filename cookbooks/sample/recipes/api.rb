%w{ python-pip python-dev screen }.each do |p|
	package p
end

bash "install-requirements" do
	cwd "#{node[:base_folder]}"
	code <<-EOH
		pip install -r requirements.txt
	EOH
	user "root"
	action :run
end

template "/etc/init/flaskapi.conf" do
	source "flaskapi.conf.erb"
	user "root"
	group "root"
end

bash "start-flaskapi" do
	code <<-EOH
		service flaskapi restart
	EOH
	user "root"
	action :run
end