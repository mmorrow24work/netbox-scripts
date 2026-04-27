from extras.scripts import Script


class HelloJobs(Script):
    class Meta:
        name = "Hello Jobs from Git Repo"
        description = "NetBox job example"

    def run(self, data, commit):
        self.log_debug("This is from the Git repo.")
