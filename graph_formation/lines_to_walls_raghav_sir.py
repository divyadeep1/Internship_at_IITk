import json
import math

filename = "./co_ordinates_line6.json"

with open(filename, 'r') as f:
  lines = json.load(f)

for line in lines:
  line.append(1) #Weight of each line

epsilon = 8 #Every point within 4 pixel range will be considered a single point
epsilon2 = 8


wall_number = len(lines)-1

print ("Number of lines: ",len(lines))


#def parallel_and_close(line_one, line_two):
#  """Checks if 2 lines are parallel and close to one another."""
#  if math.sqrt((line_one[1]-line_two[1])**2 + (line_one[2]-line_two[2])**2) < epsilon:
#    if math.sqrt((line_one[3]-line_two[3])**2 + (line_one[4]-line_two[4])**2) < epsilon:
#      return True

#  elif math.sqrt((line_one[1]-line_two[3])**2 + (line_one[2]-line_two[4])**2) < epsilon:
#    if math.sqrt((line_one[3]-line_two[1])**2 + (line_one[4]-line_two[2])**2) < epsilon:
#      return True
#  else:
#    return False

def acceptable_d_mu_sigma(d_mu, d_sigma) :
  global eps_sigma, eps_mu

  return d_sigma < eps_sigma and d_mu < eps_mu

def check_and_fuse(line_one, line_two) :
  global wall_number

  _, x00, x01, y00, y01, w0 = line_one
  _, x10, x11, y10, y11, w1 = line_two
  
  p00 = np.array([x00, y00], dtype=np.float)
  p01 = np.array([x01, y01], dtype=np.float)
  p10 = np.array([x10, y10], dtype=np.float)
  p11 = np.array([x11, y11], dtype=np.float)

  d0 = [np.linalg.norm(p00, p10),
        np.linalg.norm(p00, p11)]
  i0 = np.argmin(d0)

  d1 = [np.linalg.norm(p01, p10),
        np.linalg.norm(p01, p11)]
  i1 = np.argmin(d1)

  d_sigma = np.abs(d0[i0] - d1[i1])
  d_mu = np.average([d0[i0], d1[i1]])
  
  if not acceptable_d_mu_sigma(d_mu, d_sigma) :
    return None

  # else process further
  wall_number += 1
  wi = wall_number

  p1_tuple = (p10, p11)
  w0 = np.average([p00, p1_tuple[i0]])
  w1 = np.average([p01, p1_tuple[i1]])
  x0, y0, x1, y1 = *w0, *w1
  
  d = np.average([d0[i0], d1[i1]])

  return [wi, x0, x1, y0, y1, d]

def parallel_and_close_2(line_one, line_two) :
  _, x00, x01, y00, y01, w0 = line_one
  _, x10, x11, y10, y11, w1 = line_two
  
  p00 = np.array([x00, y00], dtype=np.float)
  p01 = np.array([x01, y01], dtype=np.float)
  p10 = np.array([x10, y10], dtype=np.float)
  p11 = np.array([x11, y11], dtype=np.float)

  dd1 = np.min(
    [np.linalg.norm(p00, p10),
     np.linalg.norm(p00, p11)]
  )

  dd2 = np.min(
    [np.linalg.norm(p01, p10),
     np.linalg.norm(p01, p11)]
  )

  d_sigma = np.abs(dd1 - dd2)
  d_mu = np.average([dd1, dd2])
  
  return  d_sigma < eps_sigma and d_mu < eps_mu

def parallel_and_close(line_one, line_two):
  """Checks if 2 lines are parallel and close to one another."""
  d1 = math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
  d2 = math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2) # sqrt((x12 - x22)**2 + (y12 - y22))
  d3 = math.sqrt((line_one[1]-line_two[2])**2 + (line_one[3]-line_two[4])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
  d4 = math.sqrt((line_one[2]-line_two[1])**2 + (line_one[4]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
  
  if abs(d1-d2) < epsilon and (d1+d2)/2 < epsilon2:
    return True
  elif abs(d3-d4) < epsilon and (d3+d4)/2 < epsilon2:
    return True
  else:
    return False


def fuse_lines(line_one, line_two):
  """Fuses two lines into a single wall."""
  global wall_number
  wall_number += 1
  if abs(math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) -
         math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2)) < epsilon:
    weight = (math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) + 
              math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2) )/2
    return  [
      wall_number, 
      (line_one[1]+line_two[1])/2,
      (line_one[2]+line_two[2])/2,
      (line_one[3]+line_two[3])/2,
      (line_one[4]+line_two[4])/2,
      weight
    ]
  else:
    weight = (math.sqrt((line_one[1]-line_two[2])**2 + (line_one[3]-line_two[4])**2) + 
              math.sqrt((line_one[2]-line_two[1])**2 + (line_one[4]-line_two[3])**2))/2
    return [
      wall_number, 
      (line_one[1]+line_two[2])/2,
      (line_one[2]+line_two[1])/2,
      (line_one[3]+line_two[4])/2,
      (line_one[4]+line_two[3])/2,
      weight
    ]

i = 0

while i<len(lines)-1:
  lines_fused = False
  for j in range(i+1,len(lines)):
    if parallel_and_close(lines[i], lines[j]):
      wall_points = fuse_lines(lines[i],lines[j])
      lines.append(wall_points)
      print(lines[i], " and ", lines[j], "fused, new line: ",wall_points, "\n")
      lines = lines[0:i] + lines[i+1:j] + lines[j+1:]
      lines_fused = True
      break
  if not lines_fused:
    i += 1


print("New number of lines:", len(lines))
