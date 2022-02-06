import yaml
import imageio
from PIL import Image, ImageDraw, ImageFont
import numpy


class Project:
    def __init__(self) -> None:
        self.yaml = None
        self.loaded_sources = {}

    def load(self, yaml_path) -> None:
        with open(yaml_path, "r") as stream:
            try:
                self.yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(
                    f"An error occured while parsing the yaml file! LOG:\n{exc}")
                exit()

        print(self.yaml)

    def load_sources(self) -> None:
        # loads sources using their paths into memory
        for source in self.yaml["sources"]:
            io_reader = imageio.get_reader(
                self.yaml['sources'][source], "ffmpeg")

            self.loaded_sources[source] = [im for im in io_reader]

            io_reader.close()

    def render(self):
        print(
            f"Rendering - {self.yaml['projectName']} @{self.yaml['projectFps']}FPS")

        print("loading all sources")
        self.load_sources()

        print("writing to file")
        io_writer = imageio.get_writer(
            self.yaml["outputPath"], fps=self.yaml["projectFps"])

        percentage_complete = 0

        for ci, clip in enumerate(self.yaml["timeline"]):
            if clip["type"] == "video":
                for ii, im in enumerate(self.loaded_sources[clip["data"]]):
                    sized_im = Image.fromarray(im)
                    sized_im = sized_im.resize(self.yaml["projectResolution"])
                    sized_im = numpy.array(sized_im)
                    io_writer.append_data(sized_im)
                    print(
                        f"{round(percentage_complete, 2)}% completed of clip {ci+1}/{len(self.yaml['timeline'])}")
                    percentage_complete = (
                        (ii+1) / len(self.loaded_sources[clip["data"]])) * 100

            elif clip["type"] == "text":
                for i in range(clip["data"]["duration"] * self.yaml["projectFps"]):
                    bg = Image.new(
                        "RGB", self.yaml["projectResolution"], (255, 255, 255))

                    draw = ImageDraw.Draw(bg)
                    font = ImageFont.truetype(
                        clip["data"]["font"], clip["data"]["fontsize"])

                    draw.text((0, 0), clip["data"]
                              ["content"], tuple(clip["data"]["color"]), font=font)

                    bg = numpy.array(bg)

                    io_writer.append_data(bg)
