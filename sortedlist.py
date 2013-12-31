from efl.elementary.table import Table, table_pack_get, table_pack_set
from efl.elementary.label import Label
from efl.elementary.button import Button
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.5

#
# TODO ideas:
# - populate with an idler
# - custom cb func for sorting
# - display sort column in the title button
# - override Table widgets methods
# - move this over to Cython to increase performance if needed
#

class SortedList(Table):

    """

    A Table that has automatically sorted rows, with user selectable column
    sort.

    Argument "titles" is a list, with each element being a tuple:
    (<Display Text>, <Sortable>)

    Cell span is assumed to be 1 in both directions.

    Items are Elementary Widgets that can have sort data placed in their data
    dict:

        item.data["sort_data"] = data

    The data from the widgets is passed to Python sort() function, if sort data
    is not found the primary text field of the widget is used as fallback.

    """

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

        """Takes a list (or a tuple) of tuples (string, bool) and packs them to
        the first row of the table."""

        assert isinstance(titles, (list, tuple))
        for t in titles:
            assert isinstance(t, tuple)
            assert len(t) == 2
            title, sortable = t
            assert isinstance(title, basestring)
            assert isinstance(sortable, bool)

        def sort_btn_cb(button, col):
            if self.sort_column == col:
                self.reverse()
            else:
                self.sort_by_column(col)

        for count, t in enumerate(titles):
            title, sortable = t
            btn = Button(self, size_hint_weight=EXPAND_HORIZ,
                size_hint_align=FILL_HORIZ, text=title)
            btn.callback_clicked_add(sort_btn_cb, count)
            if not sortable:
                btn.disabled = True
            btn.show()
            self.pack(btn, count, 0, 1, 1)
            self.header_row.append(btn)

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
            self.sort_by_column(self.sort_column)

    def row_pack_set(self, y, new_y):

        """Changes the position of a row in the table.

        Doesn't handle sorting automatically.

        """

        for x, item in enumerate(self.rows[new_y]):
            table_pack_set(item, x, y+1, 1, 1)

    def row_unpack(self, row, delete=False):

        """Unpacks and hides, and optionally deletes, a row of items.

        The argument row can either be the row itself or its index number.

        """
        if isinstance(row, int):
            row_index = row
            row = self.rows[row]
        else:
            x, row_index, w, h = table_pack_get(row[0])

        for item in row:
            self.unpack(item)
            if delete:
                item.delete()
            else:
                item.hide()

        self.rows.pop(row_index-1)
        self.sort_by_column(self.sort_column)

    def reverse(self):
        rev_order = reversed(range(len(self.rows)))
        for y, new_y in enumerate(rev_order):
            self.row_pack_set(y, new_y)

        self.rows.reverse()

    def sort_by_column(self, col):

        assert col >= 0
        assert col < len(self.header_row)

        orig_col = [
            (i, x[col].data.get("sort_data", x[col].text)) \
            for i, x in enumerate(self.rows)
            ]
        sorted_col = sorted(orig_col, key=lambda e: e[1])
        new_order = [x[0] for x in sorted_col]

        for y, new_y in enumerate(new_order):
            self.row_pack_set(y, new_y)

        self.rows.sort(key=lambda e: e[col].data.get("sort_data", e[col].text))
        self.sort_column = col
