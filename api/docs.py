import falcon

class Docs:
    def __init__(self):
        pass

    def read_html(self, filename):
        with open(filename, 'r') as f:
            return f.read()

        return None

    async def on_get_docs(self, req, resp): #get_docs
        resp.content_type = falcon.MEDIA_HTML

        opt = req.get_param("opt", default = "api")

        content = self.read_html("docs/scalar.html")

        #content = content.replace("/template", "/template".format(opt))

        resp.text = content
        resp.status = falcon.HTTP_200

    async def on_get_template(self, req, resp): #get_template
        resp.content_type = falcon.MEDIA_HTML

        #opt = req.get_param("opt", default = "api")

        #print("html", self.fns.get(opt, "api") )

        self.def_yaml = self.read_html("docs/dms_api.yaml")

        resp.text = self.def_yaml
        resp.status = falcon.HTTP_200