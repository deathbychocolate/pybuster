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

    fake_user_agent = UserAgent()

    def __init__(self):
        self.user_agent = "Pybuster"

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
        return self.fake_user_agent.ie

    def generate_user_agent_for_firefox(self) -> str:
        """
        Returns a string that represents a User-Agent
        """
        return self.fake_user_agent.firefox

    def generate_user_agent_for_chrome(self) -> str:
        """
        Returns a string that represents a User-Agent
        """
        return self.fake_user_agent.chrome

    def generate_user_agent_for_safari(self) -> str:
        """
        Returns a string that represents a User-Agent
        """
        return self.fake_user_agent.safari

    def get_user_agent(self):
        """
        Returns the User Agent as a string type
        """
        return self.user_agent

# # SAMPLE HTTP GET HEADERS
# Host: www.google.com
# Cookie: CONSENT=PENDING+892; SOCS=CAISNQgCEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwMTI0LjAyX3AwGgJlcyAEGgYIgMvRngY; NID=511=IpVqD-lDksjO-VwZrOqsU80yVV_g_zRFGY0Y5NjmdSvVEAhWXRtzqi7oA50WwF8iPLTwuSCqTSIq8zZU5fqaCLkKc0J-BxTr6wTCIdE0pbg6PqWZUpFvvCv2caotq54vLEOw4nYjZ_qOuH0KNtxqYiphZbauFkcmrhZwZw1pSug; AEC=ARSKqsK0zp10nRvsCr0NUjEuEtLTSx9vPhsHsR4_Lgs0WxyR9VsnsjgmCg
# Cache-Control: max-age=0
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# X-Client-Data: CLvrygE=
# Sec-Fetch-Site: none
# Sec-Fetch-Mode: navigate
# Sec-Fetch-User: ?1
# Sec-Fetch-Dest: document
# Accept-Encoding: gzip, deflate
# Accept-Language: en-US,en;q=0.9

# Host: www.netflix.com
# Cookie: nfvdid=BQFmAAEBEJh_C_yh5tul26p-xhGo6IhAsvPrXYadpQglbHmCchd2XXWD4hmYaxOoE4cvIUOUsv1eXa3kl8r5PorPrFgUCJtPAJpVNdVWCZlXMd01xF2DnQ%3D%3D; SecureNetflixId=v%3D2%26mac%3DAQEAEQABABSafA5LBf4K06COZkScXxNWTc2Drdg62xQ.%26dt%3D1675890648465; NetflixId=v%3D2%26ct%3DBQAOAAEBENZHJhVIMZ23ZmL8oM1ZBfSBAA3pZd-IQtcfD9BJvm5FdBqE8Da4_v5_zRyGbiIgPc7xlgzKiOh3s4bTgnNWF_zl3Jkr0xAMNBEJNguKW60A8hMZhEBSVGxTfaNKNix73UhcqEr4JcOxB5R1J90jAsN2GAL-yzIvKTE5x5HjLUa29BkRN3H-objaa9rA8GGGuFVB2Fsr90qLvBU67a96RxiPI1BVbKOtku1jpYIez8UNlsGw6NogcbmRDDVBBDNPfS-x33Q1sKZwZgpnVxQsBn2ugZ30rDuKnilVA7d29Cu_90BkCF43qP_qpuCmIgTPalWokZ0fv9Vhvalp0mqtTwNH3xfl6j0up7aewdLYitHijdc.%26bt%3Ddev%26mac%3DAQEAEAABABS-ZfAaBKDhgKcIQ3P_aL-x3pJ8Y6JLKXM.; memclid=11da8864-5473-40db-8822-db6674cd3c02; flwssn=8bd03a73-2698-4738-8ffe-d2b19e77d928
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# Sec-Fetch-Site: none
# Sec-Fetch-Mode: navigate
# Sec-Fetch-User: ?1
# Sec-Fetch-Dest: document
# Accept-Encoding: gzip, deflate
# Accept-Language: en-US,en;q=0.9
