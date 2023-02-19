"""
A header object
"""
import random
from fake_useragent import UserAgent
import constants


class Headers:
    """
    A blueprint of all the functionality needed for HTTP Headers
    """

    user_agent = UserAgent()

    def __init__(self):
        self.user_agent = self.generate_random_user_agent()

    def generate_random_user_agent(self):
        """
        Returns a string that represents a random User-Agent defined in this file
        """
        browser_name = random.choice(constants.SUPPORTED_BROWSER_NAMES)
        if browser_name == constants.BROWSER_NAME_FIREFOX:
            user_agent = self.generate_user_agent_for_firefox()
        elif browser_name == constants.BROWSER_NAME_CHROME:
            user_agent = self.generate_user_agent_for_chrome()
        elif browser_name == constants.BROWSER_NAME_SAFARI:
            user_agent = self.generate_user_agent_for_safari()
        elif browser_name == constants.BROWSER_NAME_INTERNET_EXPLORER:
            user_agent = self.generate_user_agent_for_internet_explorer()

        return user_agent

    def generate_user_agent_for_internet_explorer(self) -> str:
        """
        Returns a string that represents a User-Agent
        """
        return self.user_agent.ie

    def generate_user_agent_for_firefox(self) -> str:
        """
        Returns a string that represents a User-Agent
        """
        return self.user_agent.firefox

    def generate_user_agent_for_chrome(self) -> str:
        """
        Returns a string that represents a User-Agent
        """
        return self.user_agent.chrome

    def generate_user_agent_for_safari(self) -> str:
        """
        Returns a string that represents a User-Agent
        """
        return self.user_agent.safari
