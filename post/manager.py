from django.db.models import Manager


class PostManager(Manager):
    def like_toggle(self, user_obj, post_obj):
        if user_obj in post_obj.liked.all():
            is_liked = False
            post_obj.liked.remove(user_obj)
        else:
            is_liked = True
            post_obj.liked.add(user_obj)
        return is_liked

    def share(self, user, parent_obj):
        if parent_obj.parent:
            original_parent = parent_obj.parent
        else:
            original_parent = parent_obj

        obj = self.model(parent=original_parent,
                         user=user,
                         content=parent_obj.content)
        obj.save()
        return obj