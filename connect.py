import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep


class Connect:
    def __init__(self, host, port, user, pas):
        self.proxy_host = host
        self.proxy_port = port  # Your proxy port
        self.proxy_user = user
        self.proxy_pas = pas
        self.manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"76.0.0"
        }
        """

        self.background_js = """
        let config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (self.proxy_host, self.proxy_port, self.proxy_user, self.proxy_pas)


    def get_chromedriver(self, use_proxy=False, user_agent=None, desired_capabilities=None):
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            plugin_file = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr('manifest.json', self.manifest_json)
                zp.writestr('background.js', self.background_js)

            chrome_options.add_extension(plugin_file)
        chrome_options.add_argument(f'desired_capabilities={desired_capabilities}')
        if user_agent:
            chrome_options.add_argument(f'--user-agent={user_agent}')

        s = Service(
            executable_path='/Users/daniiltkachenko/Desktop/My/Python/Finished_Project/Snap_Chat/chromedriver'
        )
        driver = webdriver.Chrome(
            service=s,
            options=chrome_options,
        )
        return driver


