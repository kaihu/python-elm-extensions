import random

import efl.elementary as elm
elm.init()
from efl.elementary.window import StandardWindow
from efl.elementary.label import Label
from efl.elementary.button import Button
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL

#from sortedlist import SortedList

from elmextensions import SortedList

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL

ROWS = 300
COLUMNS = 5

class derp(object):
    def __init__( self ):
        win = StandardWindow("Testing", "Elementary Sorted Table")
        win.callback_delete_request_add(lambda o: elm.exit())

        titles = []
        for i in range(COLUMNS):
            titles.append(
                    ("Column " + str(i), True if i != 2 else False)
                    )

        slist = SortedList(win, titles=titles, size_hint_weight=EXPAND_BOTH,
            size_hint_align=FILL_BOTH)

        for i in range(ROWS):
            row = []
            for j in range(COLUMNS):
                if j == 0:
                    btn = Button(slist)
                    btn.text = "Delete row"
                    btn.callback_clicked_add(
                        lambda x, y=row: slist.row_unpack(y, delete=True)
                        )
                    btn.show()
                    row.append(btn)
                else:
                    data = random.randint(0, ROWS*COLUMNS)
                    lb = Label(slist, size_hint_weight=EXPAND_BOTH,
                                size_hint_align=FILL_BOTH)
                    lb.text=str(data)
                    lb.data["sort_data"] = data
                    lb.show()
                    row.append(lb)
            slist.row_pack(row, sort=False)
        #slist.sort_by_column(1)
        slist.show()
        
        win.resize_object_add(slist)

        win.resize(600, 400)
        win.show()

if __name__ == "__main__":
    GUI = derp()
    elm.run()
    elm.shutdown()
