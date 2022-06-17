    # 駐車マークに真っ直ぐ向いていく
  def face_to_mark(self, coordinate_x):
    d = 10
    count = 0
    if 300 < coordinate_x < 340:
      stop()
      turned_theta = count*d
      return True, turned_theta
    elif coordinate_x < 300:
      turnleft(d)
      count++
    elif coordinate_x > 340:
      turnright(d)
      count++
