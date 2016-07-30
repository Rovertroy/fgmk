from PIL import Image
from PIL.ImageQt import ImageQt

from fgmk import tMat, getdata, current_project, alpha_composite

emptyTile = Image.open(getdata.path('emptyTile.png'))

class TileSet:
    def __init__(self, image_file, tilePalette=None):
        self.fakefolder = False
        if(current_project.settings['gamefolder'] == ''):
            self.fakefolder = True

        if tilePalette is None:
            self.initWithoutPalette(image_file)
        else:
            self.initWithPalette(image_file, tilePalette)

    def initWithoutPalette(self, image_file):
        self.tileset = []
        self.boxsize = 32
        self.imageFile = Image.open(image_file)
        if self.imageFile.size[0] % self.boxsize == 0 and self.imageFile.size[1] % self.boxsize == 0:
            currentx = 0
            currenty = 0
            tilei = 0
            while currenty < self.imageFile.size[1]:
                while currentx < self.imageFile.size[0]:
                    imageTemp = self.imageFile.crop(
                        (currentx, currenty, currentx + self.boxsize, currenty + self.boxsize))
                    self.tileset.append([imageTemp, imageTemp.resize((self.boxsize * 2, self.boxsize * 2), Image.NEAREST),
                                         imageTemp.resize((int(self.boxsize * 0.5), int(self.boxsize * 0.5)), Image.NEAREST)])
                    tilei += 1
                    currentx += self.boxsize
                currenty += self.boxsize
                currentx = 0

    def initWithPalette(self, image_file, tilePalette):
        self.tileset = []
        self.boxsize = 32
        bxsz = self.boxsize
        self.tilePalette = tilePalette
        v = self.tilePalette

        if(self.fakefolder):
            self.imageFile = Image.open(getdata.path('tile.png'))
        else:
            self.imageFile = Image.open(image_file)
        if self.imageFile.size[0] % self.boxsize == 0 and self.imageFile.size[1] % self.boxsize == 0:
            if isinstance(self.tilePalette, dict):
                # remember: crop uses (( and )) because it is converting the
                # elements inside in coordinates
                self.tileset.append(emptyTile)
                sorted_keys = sorted(self.tilePalette, key=int)
                for k in sorted_keys:
                    #print("P Type= ", k, "  X= " ,v[k][0], "  Y= " , v[k][1])
                    #self.tileset.append( self.imageFile.crop((bxsz*v[k][0],bxsz*v[k][1],bxsz*v[k][0] + bxsz, bxsz*v[k][1] + bxsz)) )
                    imageTemp = self.imageFile.crop(
                        (bxsz * v[k][0], bxsz * v[k][1], bxsz * v[k][0] + bxsz, bxsz * v[k][1] + bxsz))
                    self.tileset.append([imageTemp, imageTemp.resize(
                        (bxsz * 2, bxsz * 2), Image.NEAREST), imageTemp.resize((int(bxsz * 0.5), int(bxsz * 0.5)), Image.NEAREST)])


colisionSet = TileSet(getdata.path('collisionTiles.png'))
eventSet = TileSet(getdata.path('eventTiles.png'))
indicativeSet = TileSet(getdata.path('indicativeTiles.png'))
clearTile = TileSet(getdata.path('clearTile.png'))