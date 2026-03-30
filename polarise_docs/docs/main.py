import os

def define_env(env):
    @env.macro
    def read_html(path):
        """Embed a pre-rendered HTML snippet inline in a Markdown page."""
        full_path = os.path.join(env.project_dir, "docs", path)
        with open(full_path, encoding="utf-8") as f:
            return f.read()
