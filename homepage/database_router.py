class DatabaseAppsRouter(object):
    EXCLUDE_MODELS = set(['view_log', 'like_log', 'comment', 'blog','user'])

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # print db, app_label, model_name, hints
        # print not (str(model_name) in self.EXCLUDE_MODELS)
        return not (str(model_name) in self.EXCLUDE_MODELS)
