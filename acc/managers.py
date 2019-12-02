from django.db.models import Manager


class UserManager(Manager):

    def is_following(self, user, other_user):
        if other_user in user.following.all():
            return True
        else:
            return False

    def toggle_follow(self, user, to_toggle_user):
        if to_toggle_user in user.following.all():
            user.following.remove(to_toggle_user)
            added = False
        else:
            user.following.add(to_toggle_user)
            added = True
        return added

    def get_by_natural_key(self, email):
        return self.get(email=email)
