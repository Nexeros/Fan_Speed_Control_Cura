from ..Script import Script

class FanSpeedControl(Script):
    def init(self):
        super().init()

    def getSettingDataString(self):
        return """{
            "name": "Fan Speed Control",
            "key": "FanSpeedControl",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "start_layer":
                {
                    "label": "Start Layer",
                    "description": "The layer number at which to start the gradual increase in fan speed",
                    "type": "int",
                    "default_value": 5
		},
                "start_speed":
                {
                    "label": "Start Speed",
                    "description": "The initial fan speed in percents % (0-100)",
                    "type": "int",
                    "default_value": 20
                },
                "end_speed":
                {
                    "label": "End Speed",
                    "description": "The final fan speed in percents % (0-100). It is recommended to set it the same as regular speed",
                    "type": "int",
                    "default_value": 100
                },
                "end_layer":
                {
                    "label": "End Layer",
                    "description": "The layer number at which to end the gradual increase in fan speed. It is recommended to set it the same as Regular fan speed at layer",
                    "type": "int",
                    "default_value": 20
                }
            }
        }"""

    def execute(self, data: list):
        start_layer = self.getSettingValueByKey("start_layer")
        end_layer = self.getSettingValueByKey("end_layer")
        start_speed = self.getSettingValueByKey("start_speed")
        end_speed = self.getSettingValueByKey("end_speed")
        start_speed_1 = (start_speed / 100) * 255 + 1
        end_speed_1 = (end_speed / 100) * 255 + 1
        start_speed_2 = round(start_speed_1)
        end_speed_2 = round(end_speed_1)

        start_layer_1 = start_layer + 2
        end_layer_1 = end_layer + 1
        current_layer = 1
        for current_layer, layer in enumerate(data):
            lines = layer.split("\n")
            for i, line in enumerate(lines):
                if "M106" in line and current_layer <= start_layer_1:
                    lines[i] = line.replace("M106", ";M106")
                if "M106" in line and current_layer >= start_layer_1 and current_layer <= end_layer_1:
                    speed = start_speed_2 + (end_speed_2 - start_speed_2) * (current_layer - start_layer_1) / (end_layer_1 - start_layer_1)
                    speed_1 = round(speed, 1)
                    lines[i] = "M106 S" + str(speed_1)
            data[current_layer] = "\n".join(lines)

        return data