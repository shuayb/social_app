from django.contrib import admin


class SocialAppAdminSite(admin.AdminSite):
    site_header = "SocialApp Admin"
    site_title = "SocialApp Admin Portal"
    index_title = "Welcome to SocialApp Portal"
