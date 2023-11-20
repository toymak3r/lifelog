from datetime import date, datetime


class Daylog:
    """
    A class representing a daily log.

    Attributes:
        template (str): The filename of the log template.
        config (str): The filename of the configuration file.
        env (Environment): An instance of the Environment class from the jinja2 library.
        version (str): The version of the log.

    Methods:
        load(): Loads the log template using the env object and stores it in the daylog attribute.
        update(): Updates the log content by rendering the template with the current date, version, and last update time.
        save(): Prints the log content.
    """

    def __init__(self, template, config, env):
        self.env = env
        self.template = template
        self.config = config
        self.version = '0.1'

    def load(self):
        """
        Loads the log template using the env object and stores it in the daylog attribute.
        """
        self.daylog = self.env.get_template(self.template)
        self.update()
    
    def update(self):
        """
        Updates the log content by rendering the template with the current date, version, and last update time.
        """
        actual_date = date.today()
        self.content = self.daylog.render(actual_date=actual_date,
                                          version=self.version,
                                          last_update=datetime.now())

    def save(self):
        """
        Prints the log content.
        """
        print(self.content)

