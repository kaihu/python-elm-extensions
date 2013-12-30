from efl.elementary.table import Table, table_pack_get, table_pack_set
from efl.elementary.label import Label
from efl.elementary.button import Button
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.5

# Argument "titles" is a list, with each element being a tuple:
# (<Display Text>, <Sortable>)

# Note: Cell span is assumed to be 1 in both directions

class SortedList(Table):
    def __init__(self, parent_widget, titles=None, initial_sort=0):

        self.header = titles
        self.sort_column = initial_sort

        self.rows = []
        self.header_row = []

        Table.__init__(self, parent_widget, size_hint_weight=EXPAND_BOTH,
            size_hint_align=FILL_BOTH, homogeneous=True)

        if titles is not None:
            self.header_row_pack(titles)

    def header_row_pack(self, titles):
        for count, title in enumerate(titles):
            btn = Button(self, size_hint_weight=EXPAND_HORIZ,
                size_hint_align=FILL_HORIZ, text=title[0])
            btn.callback_clicked_add(self.sort_btn_cb, count)
            if not title[1]:
                btn.disabled = True
            btn.show()
            self.pack(btn, count, 0, 1, 1)
            self.header_row.append(title[0])

    def row_pack(self, row, sort=True):

        """Takes a list of items and packs them to the table."""

        assert len(row) == len(self.header_row), (
            "The row you are trying to add to this sorted list has the wrong "
            "number of items! expected: %i got: %i" % (
                len(self.header_row), len(row)
                )
            )

        for count, col in enumerate(row):
            self.pack(col, count, len(self.rows)+1, 1, 1)

        self.rows.append(row)

        if sort:
            self.sort(self.sort_column)

    def row_pack_set(self, y, new_y):

        """Changes the position of a row in the table"""

        for x, item in enumerate(self.rows[new_y]):
            table_pack_set(item, x, y+1, 1, 1)

    def sort_btn_cb(self, button, col):
        if self.sort_column == col:
            self.reverse()
        else:
            self.sort(col)

    def reverse(self):
        rev_order = reversed(range(len(self.rows)))
        for y, new_y in enumerate(rev_order):
            self.row_pack_set(y, new_y)

        self.rows.reverse()

    def sort(self, col):
        orig_col = [(i, x[col].data.get("sort_data", x[col].text)) for i, x in enumerate(self.rows)]
        sorted_col = sorted(orig_col, key=lambda e: e[1])
        new_order = [x[0] for x in sorted_col]

        for y, new_y in enumerate(new_order):
            self.row_pack_set(y, new_y)

        self.rows.sort(key=lambda e: e[col].data.get("sort_data", e[col].text))
        self.sort_column = col
