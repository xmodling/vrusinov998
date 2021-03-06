class help_menu():
    commands = []
    def AddCommand(self, command, desc):
        self.command = command
        self.desc = desc
        self.commands.append(f"{self.command}  -  {self.desc}")
        return self.commands
