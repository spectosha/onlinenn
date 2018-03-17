from django.shortcuts import render

def cabinet(requset):
	return render(requset, 'cabinet/Cabinet.html', {'pagename': 'Profile',
													'subpage': 'Research',
													})

def cabinet_nn(requset):
	return render(requset, 'cabinet/Cabinet.html', {'pagename': 'Profile',
													'subpage': 'CabinetNN',
													})

def settings(requset):
	return render(requset, 'cabinet/Cabinet.html', {'pagename': 'Settings',
													'subpage': 'Contacts',
													})

def settings_sequrity(requset):
	return render(requset, 'cabinet/Cabinet.html', {'pagename': 'Settings',
													'subpage': 'Sequrity',
													})