from gunicorn.app.base import BaseApplication
 
class Application(BaseApplication):
    def load_config(self):
        s = self.cfg.set
        s('bind', "0.0.0.0:5000")
        s('workers', 4)
        s('timeout', 60)
 
    def load(self):
        from server import app
        return app
 
if __name__ == '__main__':
    Application().run()
