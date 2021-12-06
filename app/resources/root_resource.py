class RootResource:
    def on_get(self, req, resp):
        req.context.result = {
            "200 OK": "Your API is up successfully"
        }
