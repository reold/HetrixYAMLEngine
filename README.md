# Hetrix YAML engine

Hetrix is a video editor written in python. This project allows you to create and edit videos using YAML files.

## YAML!?

Yes, YAML files. The engine uses the data in the YAML file to manipulate videos.

### Additional information:

Hetrix is currently in early stages. Please note that any major change maybe made anytime.

The documentation will be updated after a stable release.

###### Working(for nerds): In the YAML file, the project details like the FPS, Resolution etc are set. It will also include paths to resources like videos and images and a timeline struct which will contain the structure of the final render. All this data will be parsed by Python. Objects like Text etc are handled by PIL image manipulation library. The read/write work is handled by ImageIO
