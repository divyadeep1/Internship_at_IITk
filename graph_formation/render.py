import logging as lg
lg.basicConfig(level=lg.DEBUG, format='%(levelname)-8s: %(message)s')

import sys
import numpy as np
import cv2
import os
import random
import yajl
from datetime import datetime as Dt

from argparse import ArgumentParser as Parser
parser = Parser()
parser.add_argument('-i', '--image', type=str)
parser.add_argument('-l', '--lines-json', type=str)
parser.add_argument('-w', '--walls-json', type=str)
parser.add_argument('-o', '--output-walls', type=str)
parser.add_argument('--output-lines', '--ol', type=str)
parser.add_argument('-W', '--force-width', type=int)

args = parser.parse_args()

lg.info("Args:\n %s", str(vars(args)).replace(", '", ",\n  '"))

image_name = args.image
walls_name = args.walls_json
lines_name = args.lines_json
out_walls = args.output_walls
out_lines = args.output_lines
W = args.force_width
image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
if image is not None :
  lg.info('Read image:%s, size: %s',
          image_name, image.shape)
else :
  lg.error('Error reading image: %s', image_name)
  lg.info('Nothing to do. Exiting.')
  sys.exit(64)

if walls_name :
  with open(walls_name, 'r') as J :
    walls = yajl.load(J)
  
  walls = np.array(walls, dtype=np.float)
  lg.info('Read walls:%s, size:%s',
          walls_name, walls.shape)
  r_idx = random.randrange(walls.shape[0])
  wall = walls[-1]
  
  _, p0_x, p1_x, p0_y, p1_y, w = wall
  
  lg.info(wall)
  lg.info("Wall #%d: p0:(%.3f, %.3f) p1:(%.3f, %.3f) w:%.3f",
          r_idx, p0_x, p0_y, p1_x, p1_y, w)
  
else :
  lg.warning('No walls json. Not reading walls.')

if out_walls and walls_name :
  new_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
  
  for _, p0_x, p1_x, p0_y, p1_y, w in walls :
    p0 = int(p0_x), int(p0_y)
    p1 = int(p1_x), int(p1_y)
  
    w = int(w) if not W else W
    # lg.debug('Given line width: %s', w)
  
    if w < 1 :
      lg.warning('Zero width line: %s, %s', p0, p1)
  
    cv2.line(new_image, p0, p1, (random.randint(40,255),random.randint(1,255),random.randint(1,255)), w)
  
  cv2.imwrite(out_walls, new_image)
else :
  lg.warning('No walls json OR no output walls. Not rendering walls.')

if lines_name :
  with open(lines_name, 'r') as J :
    lines = yajl.load(J)
  
  lines = np.array(lines, dtype=np.float)
  lg.info('Read lines:%s, size:%s',
          lines_name, lines.shape)
  r_idx = random.randrange(lines.shape[0])
  line = lines[r_idx]
  
  _, p0_x, p1_x, p0_y, p1_y = line
  
  lg.info(line)
  lg.info("Line #%d: p0:(%.3f, %.3f) p1:(%.3f, %.3f)",
          r_idx, p0_x, p0_y, p1_x, p1_y)
  
else :
  lg.warning('No lines json. Not reading lines.')

if out_lines :
  new_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
  
  for _, p0_x, p1_x, p0_y, p1_y in lines :
    p0 = int(p0_x), int(p0_y)
    p1 = int(p1_x), int(p1_y)
  
    cv2.line(new_image, p0, p1, (255,255,0), 1)
  
  cv2.imwrite(out_lines, new_image)
else :
  lg.warning('No lines json or no output lines. Not rendering lines.')
