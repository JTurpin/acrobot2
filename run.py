# -*- coding: utf-8 -*-

from acrobot.app import create_app
app, _ = create_app()  # NOQA

if __name__ == "__main__":
    app.run()
