"""
Transforme les ressources originales vers des ressources optimisées pour l'exécution.
"""

import os
from tempfile import NamedTemporaryFile

import numpy
from PIL import Image


def bake_texture(name: str):
	"""
	Transforme une texture 16x16 en une texture 2048x2048 pour OpenGL.
	"""

	print(f"Baking '{name}'...")

	input = "../res/img/" + name
	output = "../res/img/" + name + ".baked"

	f = NamedTemporaryFile(prefix="wolfenstein_", suffix=".png", delete=False)
	f.close()

	if os.system(f"convert '{input}' -scale 2048 'PNG24:{f.name}'") != 0:
		raise "Convert failed"

	bytes = numpy.array(Image.open(f.name).getdata(), numpy.uint8)
	bytes.dump(output)

	os.unlink(f.name)


if __name__ == "__main__":
	bake_texture("img.png")
