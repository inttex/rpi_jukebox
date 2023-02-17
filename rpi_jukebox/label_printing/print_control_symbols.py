# This file is part of pylabels, a Python library to create PDFs for printing
# labels.
# Copyright (C) 2014 Blair Bonnett
#
# pylabels is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pylabels is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pylabels.  If not, see <http://www.gnu.org/licenses/>.
import glob
import os
import struct
from pathlib import Path
from typing import NamedTuple

import labels
from reportlab.graphics.shapes import Drawing, Image, Group

from reportlab.graphics import shapes
from reportlab.lib import colors

# Create an A4 portrait (210mm x 297mm) sheet with 2 columns and 8 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(210, 297, 2, 5, 83.8, 50.8, corner_radius=2,
                             left_margin=18.64,
                             # column_gap=5.08,
                             right_margin=18.64,
                             top_margin=21.5,
                             row_gap=0,
                             # bottom_margin=21.5,
                             )


class LabelConfig(NamedTuple):
    title: str
    img_path: Path


draw_solid_fill = False


def get_image_info(data):
    if is_png(data):
        w, h = struct.unpack('>LL', data[16:24])
        width = int(w)
        height = int(h)
    else:
        raise Exception('not a png image')
    return width, height


def is_png(data):
    return True
    # return (data[:8] == '\211PNG\r\n\032\n' and (data[12:16] == 'IHDR'))


# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
def draw_label(label, width, height, config: LabelConfig):
    # Draw a solid background.
    if draw_solid_fill:
        r = shapes.Rect(0, 0, width, height)
        r.fillColor = colors.Color(*[0.9] * 3)
        r.strokeColor = None
        label.add(r)

    dr = Drawing()
    dirname = os.path.dirname(__file__)
    file2 = os.path.join(dirname, config.img_path)

    with open(file2, 'rb') as f:
        data = f.read()
    width, height = get_image_info(data)

    img_height = 75
    img_width = img_height * width / height
    dr.add(Image(0, 0, img_width, img_height, file2))
    string = shapes.String(0, -20, config.title, fontName="Helvetica", fontSize=20)

    group = Group(dr, string)
    img_border = 35
    group.translate(img_height + img_border, +72.5 - img_width / 2)
    group.rotate(90)

    label.add(group)


def create_sheet_1_page(my_labels, pdf_filename, draw_border=False):
    # Create the sheet.
    sheet = labels.Sheet(specs, draw_label, border=draw_border)

    # Mark some of the labels on the first page as already used.
    # sheet.partial_page(1, ((1, 1), (2, 2), (4, 2)))

    if len(my_labels) > 10:
        print('WARNING: more than 10 labels found!')

    for label in my_labels:
        sheet.add_label(LabelConfig(*label))

    # Save the file and we are done.
    sheet.save(Path('pdfs/' + pdf_filename).as_posix())
    print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))


def main():
    # https: // fontawesome.com / icons / play - pause?s = solid & f = classic
    files = glob.glob('symbols/*.png')

    my_labels = [('', Path(file)) for file in files]
    print(my_labels)

    create_sheet_1_page(my_labels, "control_symbols_labels.pdf", draw_border=False)


if __name__ == '__main__':
    main()
