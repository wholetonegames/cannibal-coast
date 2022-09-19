import bpy
import math

def create_empty(w, h):
    total = w * h

    for i in list(range(total)):
        x = (i % w) * 2
        y = math.floor(i / w) * -2
        bpy.ops.object.empty_add(type='PLAIN_AXES',
                                 view_align=False,
                                 location=(x, y, 0.0))
        # print('i', i,'x',x,'y',y)
        i_str = str(i).zfill(5)
        bpy.context.active_object.name = 'block.{}'.format(i_str)


if __name__ == "__main__":
    create_empty(25, 15)
