class HeaderandCookie:
    def __init__(self):
        self._header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
                           "X-Goog-Visitor-Id": "CgtsSVk1S1VtMTJ3YyiCvpqBBg%3D%3D",
                           "X-Goog-AuthUser": "0",
                           "x-origin": "https://www.youtube.com",
                           "X-Youtube-Identity-Token": "QUFFLUhqbmwyT2hVcFRCYVdqV1VLTkROaFY4SEZiOVdUZ3w="
                           }
        self._cookie = {
                        "__Secure-3PAPISID": "C60dEL-Ulr_fa68_/AP-IjIgUHrHBS4oXE",
                        "__Secure-3PSID": "4geB9v-jsi1F24XosdFWv166-fZWaC_wl7g0fBhibGX6tnaxrj0Pxt0H7eSKZK2eruRlRw.",
                        "__Secure-3PSIDCC": "AJi4QfGIblrY3aTE3-28Tqk9Yi2UHK-WlBNEioJsIU-ps0CY7VopxmfaU_phfZDN69Y9sWdrhOY",
                        "CONSENT": "YES+GB.en+20150726-13-0",
                        "LOGIN_INFO": "AFmmF2swRQIhAOUjmIUvN0F7zp6g1aRH-P-hHgeDhcPMvhmz9QS49Q66AiA3NZjIjvVHVSqYrTreV6_FnD_ZDkr7Lta2X_fG3L08NQ:QUQ3MjNmeVZRMFNTYm5vWUprckNlSzVsQURwZVpEaHprSHR6VVZqV3U4Z0xFUkEyaFVPbkNReXB1MGNVQzVVbW1ZMTNfdEhrbkZKcnZfZERFcnVpcDZzSkV2bkNERURONTNHNFlzU1pYbUhxWnNZaFJESUhjQzdWVkJKSnZPS1dpUXVjb1dQNW9mQnRXVmZHTkZiMVhCMWcxVVpoTGxXSFNWdjQ4NWU0S2pWYVpCcWlkVkd2akR4end3UXBmUEZ1S0hzU0hKLTZzazRBMDJsUGdPSU1xc1dtWkRMWDRyQWQ2OTMzNUdYR1ppdXd0NzJxcURxdkFKb0dGWFNCUDFnYWs4VER1ekU3NHpfUQ==",
                        "PREF": "f6=400&cvdm=grid&tz=Asia.Kolkata&al=en-GB&f5=30",
                        "VISITOR_INFO1_LIVE": "lIY5KUm12wc",
                        "YSC": "oACjWmARqD0"
                        }

    def get_cookie(self):
        return self._cookie
    def get_header(self):
        return self._header