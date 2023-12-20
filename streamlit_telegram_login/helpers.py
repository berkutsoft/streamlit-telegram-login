import os
import yaml
from yaml.parser import ParserError

ERROR_CONFIG_FILE_PATH = "File not found at the specified path: {}"
ERROR_WRONG_FORMAT = "Wrong format config: {} Please see the example in \"config.yaml\""


class YamlConfigError(Exception):
    pass


class YamlConfig:

    def __init__(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise YamlConfigError(ERROR_CONFIG_FILE_PATH.format(file_path))
        try:
            with open(file_path) as file:
                self.config = yaml.load(file, Loader=yaml.SafeLoader)
        except ParserError as ex:
            raise YamlConfigError(ex)
        self.__validate_and_update_config()

    def __validate_and_update_config(self):
        if 'widget' not in self.config:
            raise YamlConfigError(ERROR_WRONG_FORMAT.format('Param "widget" is required'))
        cfg_widget = self.config['widget']
        if cfg_widget is None or 'bot_username' not in cfg_widget:
            raise YamlConfigError(ERROR_WRONG_FORMAT.format('"bot_username" is required.'))

        if 'button_style' in cfg_widget and cfg_widget['button_style'] not in ("large", "medium", "small"):
            raise YamlConfigError(
                ERROR_WRONG_FORMAT.format('"button_style" must only take the values "large", "medium" or "small".')
            )

        if 'userpic' in cfg_widget and not isinstance(cfg_widget['userpic'], bool):
            raise YamlConfigError(ERROR_WRONG_FORMAT.format('"userpic" must accept only boolean type.'))

        if cfg_widget.get('corner_radius') and not isinstance(cfg_widget['corner_radius'], int):
            raise YamlConfigError(ERROR_WRONG_FORMAT.format('"corner_radius" must accept only null or integer type.'))

        if 'request_access' in cfg_widget and not isinstance(cfg_widget['request_access'], bool):
            raise YamlConfigError(ERROR_WRONG_FORMAT.format('"request_access" must accept only boolean type.'))
        updated_config = cfg_widget.copy()

        if cfg_cookie := self.config.get('cookie'):
            if not isinstance(cfg_cookie.get('expiry_days'), (int, float)):
                raise YamlConfigError(ERROR_WRONG_FORMAT.format('"expiry_days" must accept only integer type.'))
        else:
            cfg_cookie = {"expiry_days": 30}
        updated_config.update(cfg_cookie)

        if not self.config.get("secret_key"):
            raise YamlConfigError(ERROR_WRONG_FORMAT.format('"secret_key" is required.'))
        updated_config["secret_key"] = self.config["secret_key"]
        self.config = updated_config
