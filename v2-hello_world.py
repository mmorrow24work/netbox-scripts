from extras.scripts import Script


class HelloWorld(Script):
    class Meta:
        name = "Hello World"
        description = "A minimal NetBox Custom Script example."

    def run(self, data, commit):
        # `commit` indicates whether DB changes will be written (dry-run vs commit)
        self.log_info("Hello, World! 👋")
        self.log_success(f"Commit mode is: {commit}")
        return "Hello World completed"
