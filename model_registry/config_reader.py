from configparser import ConfigParser
import os

class ConfigReader:

    def __init__(self) -> None:
        self._config = ConfigParser()

    def read_config_file(self, ini_path: str) -> ConfigParser:
        """
        Gets the parser of the configuration file

        Parameters
        ----------
        ini_path : str
            .ini file absolute path

        Returns
        -------
        config : ConfigParser
            Configuration file parser
        """
        self._config.read(ini_path)

        return self._config